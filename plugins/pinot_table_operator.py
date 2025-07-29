import glob
import requests
import fastapi

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class PinotTableSubmitOperator(BaseOperator):
    @apply_defaults
    def __init__(self, folder_path, pinot_url, *args, **kwargs):
        super(PinotTableSubmitOperator, self).__init__(*args, **kwargs)
        self.folder_path = folder_path
        self.pinot_url = pinot_url

    def execute(self, context):
        try:
            table_files = glob.glob(self.folder_path + "/*.json")
            for table_file in table_files:
                with open(table_file, 'r') as file:
                    table_data = file.read()

                    headers = {'Content-Type': 'application/json'}
                    response = requests.post(self.pinot_url, data=table_data, headers=headers)

                    if response.status_code == 200:
                        self.log.info(f'Pinot table submitted to Apache Pinot! {table_file}')
                    else:
                        self.log.error(f'Pinot table failed to submit to Apache Pinot! {response.status_code} - {response.text}')
                        raise Exception(f'Table submission failed with status code {response.status_code}')

        except Exception as e:
            self.log.error(f'An error occured: {str(e)}')