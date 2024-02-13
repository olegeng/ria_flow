import docker
import os
import datetime

def create_postgresql_dump(source_container_name, target_container_name, username, password, database, output_dir):
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dump_file = f"{database}_dump_{current_datetime}.sql"

    client = docker.from_env()
    
    try:
        # Виконуємо pg_dump в контейнері, де запущений PostgreSQL
        source_container = client.containers.get(source_container_name)
        dump_command = f"pg_dump --username={username} --dbname={database} --format=plain"
        exit_code, output = source_container.exec_run(dump_command, user='postgres')

        if exit_code == 0:
            # Зберігаємо дамп на локальній машині
            with open(os.path.join(output_dir, dump_file), 'wb') as f:
                f.write(output)
                
            print(f"Дамп бази даних {database} був створений успішно: {os.path.join(output_dir, dump_file)}")

            # Тепер, якщо потрібно, можна скопіювати файл дампу у інший контейнер або зробити його доступним за допомогою Docker volume
            # Наприклад, щоб скопіювати дамп у цільовий контейнер, можна використати наступний код:
            target_container = client.containers.get(target_container_name)
            target_container.exec_run(f"mkdir -p /dump")
            target_container.put_archive("/dump", f"{output_dir}/{dump_file}")
            print(f"Дамп бази даних скопійовано в контейнер {target_container_name}")
        else:
            print(f"Помилка при створенні дампу: {output}")
    except docker.errors.APIError as e:
        print(f"Помилка API Docker: {e}")

# Задані параметри
source_container_name = "source_pg_db"
target_container_name = "pg_db"
username = "root"
password = "root"
database = "my_db"
output_dir = "./dumps"

# Виклик функції для створення дампу
create_postgresql_dump(source_container_name, target_container_name, username, password, database, output_dir)
