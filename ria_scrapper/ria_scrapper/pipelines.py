# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
#from logger_config import logging
import psycopg2
from psycopg2 import Error
import configparser
import pandas as pd
#logging.info('Starting scrapy Pipeline')
class RiaScrapperPipeline:
    def process_item(self, item, spider):
        return item


class SQLitePipeline:
    #logging.info('Loading to SQL')
    def open_spider(self, spider):
        #logging.info('Spider opened - SQLitePipeline')
        pass

    def close_spider(self, spider):

        def read_config(self, file_path):
            config = configparser.ConfigParser()
            config.read(file_path)
            return config['postgresql']

        def insert_data(config, data):
            try:
                connection = psycopg2.connect(user=config['username'],
                                            password=config['password'],
                                            host=config['host'],
                                            port=config['port'],
                                            database=config['database'])
                cursor = connection.cursor()
                insert_query = f""" INSERT INTO {config['database']} (url, title, price_usd, odometer, username, phone_number, image_url, images_count, car_number, car_vin, datetime_found) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

                cursor.execute(insert_query, data)
                connection.commit()
                print("Дані успішно вставлені")

            except (Exception, Error) as error:
                print("Помилка при вставці даних:", error)

            finally:
                if connection:
                    cursor.close()
                    connection.close()
                    print("Підключення закрито")

        # Шлях до файлу конфігурації
        config_file_path = '../../.en_v.cfg'

        # Читання конфігураційних даних з файлу
        config = read_config(config_file_path)

        
        df = pd.read_csv('../car.csv')
        for index, row in df.iterrows():
            car_data = row.tolist()
            insert_data(config, car_data)
            print("Рядок успішно вставлено")
        #logging.warning('Spider closed - SQLitePipeline')
        return item
    #logging.info('Loaded')