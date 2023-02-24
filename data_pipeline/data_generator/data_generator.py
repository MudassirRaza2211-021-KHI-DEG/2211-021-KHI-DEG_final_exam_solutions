from datetime import datetime
from io import StringIO
from random import randint, choice
from uuid import uuid4

import pandas as pd
import typer
import boto3
import os


app = typer.Typer()

current_date = datetime.now()

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1",
    "Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G996U Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SM-G973U Build/PPR1.180610.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
]

SITES = ["main", "sport", "fashion", "lifestyle", "tech", "business", "health"]


def generate_user_cookies(min_num: int, max_num: int):
    users = randint(min_num, max_num)
    return [uuid4().hex for _ in range(users)]


@app.command()
def run_datagen(
    bucket_name: str = typer.Argument(
        ..., help="Name of the bucket that should be filled with data"
    ),
    year: int = typer.Option(current_date.year, help="Year for which generate data"),
    month: int = typer.Option(current_date.month, help="Month for which generate data"),
    day: int = typer.Option(current_date.day, help="Day for which generate data"),
    hour: int = typer.Option(
        current_date.hour - 1, help="Hour for which generate data"
    ),
    min_rows: int = typer.Option(500000, help="Min number of generated rows"),
    max_rows: int = typer.Option(1000000, help="Max number of generated rows"),
):
    """
    Simple script for generating data required to solve your assignment.
    """

    s3 = boto3.client(
        "s3",
        endpoint_url=os.environ.get("S3_ENDPOINT_URL"),
        aws_access_key_id=os.environ.get("MINIO_ROOT_USER"),
        aws_secret_access_key=os.environ.get("MINIO_ROOT_PASSWORD"),
    )
    rows = randint(min_rows, max_rows)
    user_cookies = generate_user_cookies(rows // 60, rows // 40)
    path = f"year={year:04d}/month={month:02d}/day={day:02d}/hour={hour:02d}"
    file_num = randint(8, 12)

    typer.echo(f"Clearing path: {path}")

    response = s3.list_objects(Bucket=bucket_name, Prefix=path)
    for object in response.get("Contents", []):
        s3.delete_object(Bucket=bucket_name, Key=object["Key"])

    typer.echo(f"Removed {len(response.get('Contents', []))} objects.")

    typer.echo(f"Generating {rows} rows")

    rows_left = rows

    def get_random_row():
        return {
            "timestamp": datetime(
                year,
                month,
                day,
                hour,
                randint(0, 59),
                randint(0, 59),
                randint(0, 100000),
            ).isoformat(),
            "user_cookie": choice(user_cookies),
            "site": choice(SITES),
            "user_agent": choice(USER_AGENTS),
        }

    for i in range(file_num):
        file_rows = (
            randint(rows_left // 8, rows_left // 4) if i + 1 < file_num else rows_left
        )
        rows_left -= file_rows

        file_path = path + f"/{i + 1:06d}.csv"
        typer.echo(f"For path {file_path} generating {file_rows} rows")
        df = pd.DataFrame([get_random_row() for _ in range(file_rows)])

        s3_path = f"s3://{bucket_name}/{file_path}"
        csv_buffer = StringIO()
        df.to_csv(csv_buffer)
        s3.put_object(Bucket=bucket_name, Body=csv_buffer.getvalue(), Key=file_path)
        typer.echo(f"Saved file: {s3_path}")

    typer.echo("Creating FULL marker file")
    s3.put_object(Bucket=bucket_name, Body=b"", Key=path + "/FULL")

    typer.echo("Success! Your data is ready.")


if __name__ == "__main__":
    app()
