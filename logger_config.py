import os
import logging

def setup_logger():
    # Получение пути к текущей директории
    current_directory = os.path.dirname(os.path.abspath(__file__))
    log_file_path = os.path.join(f'{current_directory}/', 'app.log')

    # Создание объекта логгера
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)

    # Создание объекта для вывода логов в файл
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)

    # Создание форматтера для логов
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Добавление обработчика к логгеру
    logger.addHandler(file_handler)

    return logger

# Получаем готовый логгер
logger = setup_logger()
