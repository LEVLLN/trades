import datetime
from libs.connection import *


class Stock(Model):
    code = CharField(primary_key=True)
    name = CharField(unique=True)

    class Meta:
        database = DB


class Price(Model):
    stock = ForeignKeyField(Stock, backref='prices')
    date = DateField()
    open = DoubleField(default=0.0)
    high = DoubleField(default=0.0)
    low = DoubleField(default=0.0)
    close = DoubleField(default=0.0)
    volume = DoubleField(default=0.0)

    class Meta:
        database = DB


class Trade(Model):
    stock = ForeignKeyField(Stock, backref='trades')
    insider = CharField()
    relation = CharField()
    last_date = DateField()
    transaction_type = CharField()
    owner_type = CharField(choices=["direct", "indirect"])
    shares_traded = IntegerField(default=0.0)
    last_price = DoubleField(default=0.0)
    shares_held = IntegerField(default=0.0)

    class Meta:
        database = DB

# init database tables


def __create_tables__():
    DB.create_tables([Stock, Price, Trade])


if not Trade.table_exists:
    DB.create_tables(Trade)
if not Stock.table_exists:
    DB.create_tables(Stock)
if not Price.table_exists:
    DB.create_tables(Price)
