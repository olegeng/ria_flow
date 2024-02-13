FROM apache/airflow:latest

# Копіюємо файли DAG до контейнера
COPY ./__pycache__ /opt
COPY ./.env /opt
COPY ./dumps /opt
COPY ./postgres_data /opt
COPY ./ria_scrapper /opt
COPY ./dumper.py /opt
COPY ./logger_config.py /opt
COPY ./README.md /opt
COPY ./requirements.txt /opt
COPY .dump_dag.py /opt/airflow/dags
COPY .etl_dag.py /opt/airflow/dags
RUN pip install --no-cache-dir -r /app/requirements.txt
WORKDIR /opt
# Встановлюємо залежності Python, якщо вони потрібні

# Встановлюємо додаткові пакети, якщо вони потрібні
