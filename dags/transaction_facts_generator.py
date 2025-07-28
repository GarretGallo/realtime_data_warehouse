from airflow import DAG
from airflow.operators.empty import EmptyOperator
from kafka_operator import KafkaProduceOperator
from datetime import datetime, timedelta

start_date = datetime(2025, 3, 15)
default_args = {
    'owner': 'GGCODE',
    'depends_on_past': False,
    'backfill': False,
    'start_date': start_date,
}

with DAG(
    dag_id='transaction_facts_generator',
    default_args=default_args,
    description='Transaction Facts Generator',
    schedule_interval=timedelta(days=1),
    tags=['facts_data']
) as dag:
    start = EmptyOperator(task_id='start')

    generate_txn_data = KafkaProduceOperator(
        task_id = 'generate_txn_fact_data',
        kafka_broker = 'kafka_broker:9092',
        kafka_topic = 'transaction_facts',
        num_records = 100)

    end = EmptyOperator(task_id='end')

    start >> generate_txn_data >> end