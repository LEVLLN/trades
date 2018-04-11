from peewee import *
import datetime

db = PostgresqlDatabase('trades', user='postgres', password='qwerty123',
                        host='localhost', port=5432)


class Stock(Model):
    pass

    class Meta:
        database = db


class Price(Model):
    pass

    class Meta:
        database = db


class Trade(Model):
    pass

    class Meta:
        database = db


def __create_tables__():
    db.create_tables([Stock, Price, Trade])
