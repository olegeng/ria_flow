from airflow import DAG
import configparser
from airflow.operators.bash_operator  import BashOperator
from airflow.utils.dates import days_ago

def read_config(file_path):
        config = configparser.ConfigParser()
        config.read(file_path)
        return config['airflow_dump']

config_file_path = '../../.env/config.cfg'
config = read_config(config_file_path)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'execute_dumper_script',
    default_args=default_args,
    description='A DAG to execute dumper script',
    schedule_interval=f'{config['min']} {config['hour']} * * *',
    start_date=days_ago(1),
    tags=['dumper', 'script'],
)

# Оператори для виконання кожної команди
cd_command = "cd ../../"
python_command = "python3 dumper.py"

# Оператори BashOperator для виконання команд
cd_operator = BashOperator(
    task_id='change_directory',
    bash_command=cd_command,
    dag=dag,
)

python_operator = BashOperator(
    task_id='run_dumper_script',
    bash_command=python_command,
    dag=dag,
)

# Встановлюємо залежність між операторами
cd_operator >> python_operator