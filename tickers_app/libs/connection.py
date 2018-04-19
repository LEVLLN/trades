from peewee import *
from .log_writer import init_logger
APP_NAME = 'connection'
LOG_FILE_PATH = f'logs/{APP_NAME}.log'


def connect_to_db():
    try:
        data_base = PostgresqlDatabase('trades', user='postgres',
                                       password='qwerty123', host='localhost', port=5432)
        return data_base
    except Exception as db_exception:
        LOGGER.info(f'Can not connect to database: {db_exception}')


LOGGER = init_logger(LOG_FILE_PATH, APP_NAME)
db = connect_to_db()
