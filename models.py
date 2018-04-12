from peewee import *
import datetime

db = PostgresqlDatabase('trades', user='postgres', password='qwerty123',
                        host='localhost', port=5432)


class Stock(Model):
    code = CharField(primary_key=True)
    name = CharField(unique=True)

    class Meta:
        database = db

    def get_all_stocks(self):
        try:
            return self.select()
        except Exception as e:
            print(f'Can\'t get stocks: {e}')

    def create_stock(self, stock_code, stock_name):
        try:
            self.create(code=stock_code, name=stock_name)
            print(f'A stock {stock_name} has been created')
        except Exception as e:
            print(f'Can\'t create stock: {e}')

    def get_stock_by_code(self, stock_code):
        try:
            return self.get(Stock.code == stock_code)
        except Exception as e:
            print(f'Can\'t get stock {stock_code}: {e}')


class Price(Model):
    stock = ForeignKeyField(Stock, backref='prices')
    date = DateField()
    open = DoubleField(default=0.0)
    high = DoubleField(default=0.0)
    low = DoubleField(default=0.0)
    close = DoubleField(default=0.0)

    class Meta:
        database = db


class Trade(Model):
    pass

    class Meta:
        database = db


class URLParameter(object):
    stock = ""
    page_num = 1
    url_type = ""

# init database tables


def __create_tables__():
    db.createп_tables([Stock, Price])


# stock = Stock()
# # stock.create_stock('aapl', 'Apple inc.')
# print(stock.get_stock_by_code('aapl').code)
