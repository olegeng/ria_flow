from airflow import DAG
from logger_config import logging
import configparser
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
logging.info('Starting etl_dag')
config_file_path = '../../.env'

def read_config(file_path):
        config = configparser.ConfigParser()
        config.read(file_path)
        return config['airflow_etl']

config = read_config(config_file_path)
logging.info('Setting default args')
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}
logging.info('Setting dag')
dag = DAG(
    'scrape_autoria_data',
    default_args=default_args,
    description='A DAG to scrape data from autoria',
    schedule_interval=f'{config['min']} {config['hour']} * * *',
    start_date=days_ago(1),
    tags=['autoria', 'scraping'],
)

logging.info('Setting commands')
cd_command = "cd ../../ria_flow/ria_scrapper"
scrapy_command = "scrapy crawl autoria -o car.csv"

logging.info('Setting task')
cd_operator = BashOperator(
    task_id='change_directory',
    bash_command=cd_command,
    dag=dag,
)
logging.info('Setting task')
scrapy_operator = BashOperator(
    task_id='run_scrapy_crawler',
    bash_command=scrapy_command,
    dag=dag,
)

# Встановлюємо залежність між операторами
cd_operator >> scrapy_operator
