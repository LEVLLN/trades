from datetime import datetime
from models import Trade, Stock, Price, db
from page_loader import *
from page_scraper import *
from libs.log_writer import *

APP_NAME = 'data_utils'
LOG_FILE_PATH = f'logs/{APP_NAME}.log'


def save_trades(element_list, stock_code):
    for element in element_list:
        trade = Trade()
        trade.stock = stock_code
        trade.insider = element[0]
        trade.relation = element[1]
        trade_last_date = datetime.date(
            datetime.strptime(element[2], '%m/%d/%Y'))
        trade.last_date = trade_last_date
        trade.transaction_type = element[3]
        trade.owner_type = element[4]
        shares_traded = element[5].replace(',', '')
        if shares_traded == '':
            shares_traded = 0
        trade.shares_traded = shares_traded
        last_price = element[6]
        if last_price == '':
            last_price = 0.0
        trade.last_price = last_price
        shares_held = element[7].replace(',', '')
        if shares_held == '':
            shares_held = 0
        trade.shares_held = shares_held
        trade.save()
        LOGGER.info(
            f'Trade object of {stock_code} on last date {element[2]} saved in db')


def save_stock(stock):
    try:
        stock.save(force_insert=True)
    except Exception as exception:
        LOGGER.error(f'{stock.code} is allready exist: {exception}')
        db.rollback()
    LOGGER.info(f'Stock object: {stock.code} of {stock.name} saved in db')


def save_prices(element_list, stock_code):
    for element in element_list:
        price = Price()
        price.stock = stock_code
        price_date = datetime.date(datetime.strptime(element[0], '%m/%d/%Y'))
        price.date = price_date
        price.open = element[1]
        price.high = element[2]
        price.low = element[3]
        price.close = element[4]
        volume = element[5].replace(',', '')
        if volume == '':
            volume = 0
        price.volume = volume
        try:
            price.save()
            LOGGER.info(f'Price object: {price.stock} in date: {price.date} saved in db')
        except Exception as exception:
            LOGGER.error(f'{price.code} in date: {price.date} is not saved: {exception}')

LOGGER = init_logger(LOG_FILE_PATH,APP_NAME)
