"""
### Tutorial DAG for Airflow connections using the HTTP and GitHub provider

Use the GithubTagSensor to wait for a tag to be added to a GitHub repository saved
in the variable `my_github_repo`.
Once this first task succeeds the SimpleHttpOperator will query an API defined 
in an HTTP connection with the connection ID `my_http_connection`. 

This DAG's purpose is to show how to set up connections and variables in
the Get Started with Airflow - Part 2 tutorial.
"""

from airflow.decorators import dag
from airflow.models import Variable
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.github.sensors.github import GithubTagSensor
from pendulum import datetime


@dag(
    start_date=datetime(2023, 7, 1),
    schedule="0 9 * * *",
    catchup=False,
    tags=["connections"],
)
def my_second_dag():
    tag_sensor = GithubTagSensor(
        task_id="tag_sensor",
        github_conn_id="my_github_connection",
        tag_name="my_awesome_tag",
        repository_name=Variable.get("my_github_repo", "apache/airflow"),
        timeout=60 * 60 * 24,
        poke_interval=30,
    )

    query_API = SimpleHttpOperator(
        task_id="query_API",
        http_conn_id="my_http_connection",
        method="GET",
        log_response=True,
    )

    tag_sensor >> query_API


my_second_dag()
