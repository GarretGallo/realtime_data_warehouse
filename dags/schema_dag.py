import random
from datetime import datetime, timedelta

import pandas as pd
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from

start_date = datetime(2024, 9, 15)
default_args = {
    'owner': 'GGCODE',
    'depends_on_past': False,
    'backfill': False,
    'start_date': start_date,
}

with DAG(dag_id='schema_dag',
         default_args=default_args,
         description='A DAG to subit all schema in a folder to Apache Pinot',
         schedule_interval=timedelta(days=1),
         tags=['schema']) as dag:

    start = EmptyOperator(task_id='start')

    submit_schema = PinotSchemaSubmitOperator(
        task_id='submit_schema',
        folder_path = '/opt/airflow/dags/schemas',
        pinot_url = 'http://pinot-controller:9000/schemas'
    )

    end = EmptyOperator(task_id='end')

    start >>submit_schema >> end

