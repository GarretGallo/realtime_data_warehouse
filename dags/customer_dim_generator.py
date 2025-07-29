import random
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow import DAG
from datetime import datetime, timedelta
import pandas as pd

start_date = datetime(2025, 3, 15)
default_args = {
    'owner': 'GGCODE',
    'depends_on_past': False,
    'backfill': False,
}

num_rows = 100
output_file = './customer_dim_large_data.csv'

cities = ['Berlin', 'Middletown', 'Cheshire', 'Southington', 'Bristol']
regions = ['Hartford', 'New London', 'Windham', 'Fairfield', 'Middlesex']
postcodes = ['06023', '06457', '06408', '06052', '06010']

def generate_random_data(row_num):
    customer_id = f"A{row_num:05d}"
    first_name = f"FirstName{row_num}"
    last_name = f"LastName{row_num}"
    email = f"customer{row_num}@example.com"
    phone_number = f"+1-800-{random.randint(0,9999)}"

    now = datetime.now()
    random_date = now - timedelta(days=random.randint(0, 3650))
    opening_date_millis = int(random_date.timestamp()*1000)

    return customer_id, first_name, last_name, email, phone_number, opening_date_millis

customer_ids = []
first_names = []
last_names = []
emails = []
phone_numbers = []
registration_dates = []

def generate_customer_dim_data():
    row_num = 1
    while row_num <= num_rows:
        customer_id, first_name, last_name, email, phone_number, registration_date = generate_random_data(row_num)
        customer_ids.append(customer_id)
        first_names.append(first_name)
        last_names.append(last_name)
        emails.append(email)
        phone_numbers.append(phone_number)
        registration_dates.append(registration_date)
        row_num += 1

    df = pd.DataFrame({"customer_id": customer_ids,
                       "first_name": first_names,
                       "last_name": last_names,
                       "email": emails,
                       "phone_number": phone_numbers,
                       "registration_date": registration_dates})

    df.to_csv(output_file, index=False)
    print(f"CSV file '{output_file}' with {num_rows} rows created successfully!")

with DAG('customer_dim_generator',
         default_args=default_args,
         description='A DAG to generate large customer dimension data',
         schedule_interval=timedelta(days=1),
         start_date=start_date,
         tags=['dimension']) as dag:

    start = EmptyOperator(task_id='start')

    generator_customer_dimension_data = PythonOperator(
        task_id='generator_customer_dim_data',
        python_callable=generate_customer_dim_data)

    end = EmptyOperator(task_id='end',)

    start >> generator_customer_dimension_data >> end