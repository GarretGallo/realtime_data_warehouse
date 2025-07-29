import sys, os
sys.path.insert(0, os.path.join(os.environ.get("AIRFLOW_HOME","/opt/airflow"), "plugins"))

import random
from datetime import datetime, timedelta

import pandas as pd
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from pinot_table_operator import PinotTableSubmitOperator

start_date = datetime(2025, 3, 15)
default_args = {
    'owner': 'GGCODE',
    'depends_on_past': False,
    'backfill': False,
    'start_date': start_date,
}

with DAG(dag_id='table_dag',
         default_args=default_args,
         description='A DAG to submit all table in a folder to Apache Pinot',
         schedule_interval=timedelta(days=1),
         tags=['schema']) as dag:

    start = EmptyOperator(task_id='start')

    submit_tables = PinotTableSubmitOperator(
        task_id='submit_tablea',
        folder_path = '/opt/airflow/dags/tables',
        pinot_url = 'http://pinot-controller:9000/tables'
    )

    end = EmptyOperator(task_id='end')

    start >>submit_tables >> end