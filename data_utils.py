from models import Trade, Stock, Price
from models import Stock, Price, Trade
from datetime import datetime
from page_loader import *
from page_scraper import *


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


def save_stock(stock_code):
    stock = Stock()
    stock_url = make_url('main', stock_code)
    stock_page = load_page(stock_url)
    stock_name = scrape_stock_name(stock_page)
    stock.name = stock_name
    stock.code = stock_code
    stock.save(force_insert=False)
    return stock


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
        price.save()
