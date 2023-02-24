import boto3
import pandas as pd
from datetime import datetime, timedelta
import psycopg2
from psycopg2 import sql
from user_agents import parse
import time


def wait_for_full_file(bucket_name, prefix):
    start_time = time.time()
    while True:
        objects = s3.Bucket(bucket_name).objects.filter(Prefix=f"{prefix}/FULL")
        if any(objects):
            return
        if time.time() - start_time >= 600:
            raise TimeoutError("Timed out waiting for FULL file to appear.")
        print("Waiting for FULL file to appear...")
        time.sleep(60)


def read_csv_files(bucket_name, prefix):
    # Get a list of CSV file names in the directory
    objects = s3.Bucket(bucket_name).objects.filter(Prefix=prefix)
    csv_files = [obj.key for obj in objects if obj.key.endswith(".csv") and not obj.key.endswith("/FULL")]

    # Read the CSV files into a single Pandas DataFrame
    dfs = []
    for file_name in csv_files:
        obj = s3.Object(bucket_name, file_name)
        body = obj.get()["Body"]
        df = pd.read_csv(body, index_col=0)
        dfs.append(df)
    combined_df = pd.concat(dfs, ignore_index=True)

    return combined_df


def calculate_metrics(combined_df):
    # Parse the user agent strings into device type and browser columns
    ua_series = combined_df["user_agent"].apply(parse)
    combined_df["device_type"] = ua_series.apply(lambda ua: ua.device.family)
    combined_df["browser"] = ua_series.apply(lambda ua: ua.browser.family)

    # Calculate the sum of page views and unique users by site, device type, and browser
    metrics_df = combined_df.groupby(["site", "device_type", "browser"]).agg(
        {"user_cookie": "nunique", "timestamp": "count"}
    )
    metrics_df = metrics_df.rename(columns={"user_cookie": "unique_users", "timestamp": "page_views"})

    return metrics_df


def insert_to_postgresql(metrics_df, table_name, db_config):

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host=db_config["host"],
        port=db_config["port"],
        dbname=db_config["dbname"],
        user=db_config["user"],
        password=db_config["password"],
    )

    # Define the column names
    column_names = ("site", "device_type", "browser", "unique_users", "page_views")

    # Insert the data into the table
    with conn.cursor() as cur:
        for index, row in metrics_df.iterrows():
            values = (row["site"], row["device_type"], row["browser"], row["unique_users"], row["page_views"])
            insert_statement = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table_name),
                sql.SQL(", ").join(map(sql.Identifier, column_names)),
                sql.SQL(", ").join(sql.Placeholder() * len(column_names)),
            )
            cur.execute(insert_statement, values)
        conn.commit()

    # Close the database connection
    conn.close()


if __name__ == "__main__":
    # Connect to Minio using the S3 protocol
    s3 = boto3.resource(
        "s3",
        endpoint_url="http://172.26.0.3:9000",
        aws_access_key_id="minioadmin",
        aws_secret_access_key="miniopassword",
    )

    # Get the current time and construct the prefix string
    now = datetime.now()
    year, month, day, hour = now.year, now.month, now.day, now.hour - 1
    prefix = f"year={year:04d}/month={month:02d}/day={day:02d}/hour={hour:02d}"

    # Wait for the FULL file to appear in the hour-partition directory before processing the partition
    bucket_name = "test-bucket"
    wait_for_full_file(bucket_name, prefix)

    # Read the CSV files in the hour-partition directory into a single Pandas DataFrame
    combined_df = read_csv_files(bucket_name, prefix)

    # Calculate the sum of page views and unique users by site, device type, and browser
    metrics_df = calculate_metrics(combined_df)

    # Insert the metrics data into a PostgreSQL table
    table_name = "mytable"
    db_config = {
        "host": "127.0.0.1",
        "port": 5432,
        "dbname": "mydb",
        "user": "myuser",
        "password": "mypassword",
    }
    insert_to_postgresql(metrics_df, table_name, db_config) 
