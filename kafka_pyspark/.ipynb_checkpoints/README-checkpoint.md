# Kafka-Pyspark task
**For the environment see the Hints section of this document.**


In the `exam_data_preparation.ipynb` file you're given a script that reshapes the `data/titanic.csv` file data and sends it to a Kafka topic in batch mode. The data in the `titanic_topic` is nested and a sample message has the following shape:

```json
{
    'Timestamp': '2020-01-01T13:32:25.000Z',
    'string_columns': 
        {
            'Name': 'Dooley, Mr. Patrick',
            'Sex': 'male',
            'Age': '32',
            'Ticket': '370376',
            'Fare': '7.75',
            'Embarked': 'Q'
        },
  'numeric_columns':
        {
            'PassengerId': 891,
            'Survived': 0,
            'Pclass': 3,
            'SibSp': 0,
            'Parch': 0
        }
}
```

Your task is to write a notebook with PySpark code that will:
* Provide a schema to read the data from Kafka and allow to operate on the nested columns using PySpark API.
* Denest the data structure so it is flat (all columns on the same level).
* Ensure there are no duplicate rows.
* Ensure that `Cabin`, `Age` and `Embarked` columns are not null.
* Delete the `Pclass`, `SibSp`, `Parch` columns.
* Fix the types for `Age` and `Fare` columns.
* Write data as json (a textfile with multiple json lines) locally using `DataFrameWriter`.

Requirements:
* You **can't** (and don't need to) edit `exam_data_preparation.ipynb` file.
* You **can** create any other files you find useful.
* In the submission include the whole working solution – after downloading your solution we should be able to run it in JupyterLab.

Hints:
* Run Kafka cluster using `docker-compose` - see `docker-compose.yaml` file.
* Run the Jupyter Instance with the following command.
```bash
docker run \
	--network="host" \
	--user "$(id -u)" \
	--group-add users \
	--volume "${PWD}":/home/jovyan/workspace \
	jupyter/pyspark-notebook:1840ddc9dc35
```
* If you have trouble accessing the JupyterLab in the browser ensure the ports are not in use. Try running with `sudo` as well. Ultimately, switch `--network="host"` to `-p 8888:8888` (but this will require fixing communication with Kafka). You can modify `docker-compose.yml` to start Jupyter together with Kafka (as another service), then you don't need to run the command shown above.
* Ensure you add `org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1` package to `SparkSession` to allow Kafka support.
