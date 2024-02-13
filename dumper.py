import docker, configparser
import os
import datetime

def create_postgresql_dump(container_name, username, password, database, output_dir):
    # Формуємо ім'я файлу дампу з поточною датою та часом
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dump_file = f"{database}_dump_{current_datetime}.sql"
    
    # Ініціалізуємо клієнт Docker
    client = docker.from_env()
    container = client.containers.get(container_name)
    dump_command = f"pg_dump --username={username} --dbname={database} --format=plain"

    try:
        exit_code, output = container.exec_run(dump_command, user='postgres')
        if exit_code == 0:
            with open(os.path.join(output_dir, dump_file), 'wb') as f:
                f.write(output)
            print(f"Дамп бази даних {database} був створений успішно: {os.path.join(output_dir, dump_file)}")
        else:
            print(f"Помилка при створенні дампу: {output}")
    except docker.errors.APIError as e:
        print(f"Помилка API Docker: {e}")

def read_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config['postgresql']

config_file_path = './.en_v.cfg'
config = read_config(config_file_path)
container_name = config['host']
username = config['username']
password = config['password']
database = config['database']

output_dir = config['dump_folder']
create_postgresql_dump(container_name, username, password, database, output_dir)