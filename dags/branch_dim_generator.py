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

num_rows = 50
output_file = './branch_dim_large_data.csv'

cities = ['Berlin', 'Middletown', 'Cheshire', 'Southington', 'Bristol']
regions = ['Hartford', 'New London', 'Windham', 'Fairfield', 'Middlesex']
postcodes = ['06023', '06457', '06408', '06052', '06010']

def generate_random_data(row_num):
    branch_id = f"A{row_num:05d}"
    branch_name = f"Branch {row_num}"
    branch_address = f"{random.randint(1, 999)} {random.choice(['Main St', 'High St', 'Providence Ave', 'Church Rd'])}"
    city = random.choice(cities)
    region = random.choice(regions)
    postcode = random.choice(postcodes)

    now = datetime.now()
    random_date = now - timedelta(days=random.randint(0, 3650))
    opening_date_millis = int(random_date.timestamp()*1000)

    return branch_id, branch_name, branch_address, city, region, postcode, opening_date_millis

branch_ids = []
branch_names = []
branch_addresses = []
cities_list = []
regions_list = []
postcodes_list = []
opening_dates = []

def generate_branch_dim_data():
    row_num = 1
    while row_num <= num_rows:
        data = generate_random_data(row_num)
        branch_ids.append(data[0])
        branch_names.append(data[1])
        branch_addresses.append(data[2])
        cities_list.append(data[3])
        regions_list.append(data[4])
        postcodes_list.append(data[5])
        opening_dates.append(data[6])
        row_num += 1

    df = pd.DataFrame({"branch_id": branch_ids,
                       "branch_name": branch_names,
                       "branch_address": branch_addresses,
                       "city": cities_list,
                       "region": regions_list,
                       "postcode": postcodes_list,
                       "opening_date": opening_dates})

    df.to_csv(output_file, index=False)
    print(f"CSV file '{output_file}' with {num_rows} rows created successfully!")

with DAG('branch_dim_generator',
         default_args=default_args,
         description='Branch large branch dimension dara CSV file',
         schedule_interval=timedelta(days=1),
         start_date=start_date,
         tags=['schema']) as dag:

    start = EmptyOperator(task_id='start')

    generator_branch_dimension_data = PythonOperator(
        task_id='generator_branch_dim_data',
        python_callable=generate_branch_dim_data)

    end = EmptyOperator(task_id='end')

    start >> generator_branch_dimension_data >> end