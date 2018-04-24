import datetime
from peewee import *
from libs.connection import db


class Stock(Model):
    code = CharField(primary_key=True)
    name = CharField(unique=True)

    class Meta:
        database = db


class Price(Model):
    stock = ForeignKeyField(Stock, backref='prices')
    date = DateField()
    open = DoubleField(default=0.0)
    high = DoubleField(default=0.0)
    low = DoubleField(default=0.0)
    close = DoubleField(default=0.0)
    volume = DoubleField(default=0.0)

    class Meta:
        database = db


class Insider(Model):
    code = CharField(primary_key=True)
    name = CharField(unique=True)

    class Meta:
        database = db


class Trade(Model):
    stock = ForeignKeyField(Stock, backref='trades')
    insider = ForeignKeyField(Insider, backref='trades')
    relation = CharField()
    last_date = DateField()
    transaction_type = CharField()
    owner_type = CharField(choices=["direct", "indirect"])
    shares_traded = IntegerField(default=0.0)
    last_price = DoubleField(default=0.0)
    shares_held = IntegerField(default=0.0)

    class Meta:
        database = db


# init database tables


class IndividualInsiderTrades(Model):
    insider = ForeignKeyField(Insider, backref='trades')
    company = ForeignKeyField(Stock, backref='tickers')
    relation = CharField()
    last_date = DateField()
    tran = CharField()
    owner_type = CharField()
    shares_traded = DoubleField()
    last_price = DoubleField(default=0.0)
    shares_held = IntegerField(default=0.0)

    class Meta:
        database = db


def __create_tables__():
    db.create_tables([Stock, Price, Trade, Insider, IndividualInsiderTrades])

__create_tables__()