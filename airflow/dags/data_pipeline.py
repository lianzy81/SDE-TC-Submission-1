"""Airflow Data Pipeline

Defines the directed acyclic graph (DAG) for scheduling the batch execution of the data pipeline via Airflow.
"""
import os
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from plugins.preprocess import ingest_and_process_data, check_output_data_validity

from datetime import datetime

with DAG(
    dag_id="data_pipeline_dag",
    start_date=datetime(2022, 12, 14),
    schedule=None #"0 * * * *"
) as dag:

    start_task = EmptyOperator(
        task_id="start"
    )

    ingest_and_preprocess = PythonOperator(
        task_id="ingest_and_process",
        python_callable=ingest_and_process_data
    )

    validity_check = PythonOperator(
        task_id="validity_check",
        python_callable=check_output_data_validity
    )

    stop_task = EmptyOperator(
        task_id='stop'
    )

start_task >> ingest_and_preprocess >> validity_check >> stop_task