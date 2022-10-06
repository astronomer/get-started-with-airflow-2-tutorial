from airflow import DAG
from airflow.models import Variable
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.github.sensors.github import GithubTagSensor
from datetime import datetime

with DAG(
    dag_id="my_second_dag",
    start_date=datetime(2022, 9, 1),
    schedule="0 9 * * *",
    catchup=False
):

    tag_sensor = GithubTagSensor(
        task_id='tag_sensor',
        github_conn_id="my_github_connection",
        tag_name='v1.0',
        repository_name=Variable.get("my_github_repo"),
        timeout=60*60*24,
        poke_interval=30
    )

    query_API = SimpleHttpOperator(
        task_id="query_API",
        http_conn_id="my_http_connection",
        method="GET",
        log_response=True
    )

    tag_sensor >> query_API