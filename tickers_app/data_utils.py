from datetime import datetime
from models import Trade, Stock, Price, Insider, IndividualInsiderTrades, db
from page_loader import make_url,load_page
from page_scraper import *
from libs.log_writer import *

APP_NAME = 'data_utils'
LOG_FILE_PATH = f'logs/{APP_NAME}.log'


def save_trades(element_list, stock_code, insider_code):
    for element in element_list:
        trade = Trade()
        trade.stock = stock_code
        trade.insider = insider_code
        trade.relation = element[2]
        trade_last_date = datetime.date(
            datetime.strptime(element[3], '%m/%d/%Y'))
        trade.last_date = trade_last_date
        trade.transaction_type = element[4]
        trade.owner_type = element[5]
        shares_traded = element[6].replace(',', '')
        if shares_traded == '':
            shares_traded = 0
        trade.shares_traded = shares_traded
        last_price = element[7]
        if last_price == '':
            last_price = 0.0
        trade.last_price = last_price
        shares_held = element[8].replace(',', '')
        if shares_held == '':
            shares_held = 0
        trade.shares_held = shares_held
        try:
            trade.save()
            logger.info(
                f'Trade object of {stock_code} on last date {element[2]} saved in db')
        except Exception as exception:
            logger.error(f'{stock_code} is allready exist: {exception}')
            db.rollback()


def save_insider(element_list):
    for element in element_list:
        insider = Insider()
        insider.code = element[0]
        insider.name = element[1]
        try:
            insider.save(force_insert=True)
            logger.info(
                f'Insider object of {element_list[0]} --- {element[1]} saved in db')
            return insider
        except Exception as exception:
            logger.error(f'{element_list[0]} is allready exist: {exception}')
            db.rollback()
            return insider


def save_stock(stock):
    try:
        stock.save(force_insert=True)
        logger.info(f'Stock object: {stock.code} of {stock.name} saved in db')
    except Exception as exception:
        logger.error(f'{stock.code} is allready exist: {exception}')
        db.rollback()


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
            logger.info(
                f'Price object: {price.stock} in date: {price.date} saved in db')
        except Exception as exception:
            logger.error(
                f'{price.code} in date: {price.date} is not saved: {exception}')


def save_individual_trades(element_list, individual_code):
    for element in element_list:
        insider_trade = IndividualInsiderTrades()
        link = element[0]
        stock_code = link.replace('https://www.nasdaq.com/symbol/', '')
        stock_code = stock_code.replace(
            '/insider-trades', '').strip(' \t\n\r').upper()
        print(stock_code)

        try:
            Stock().get_by_id(stock_code)
            print('success')
            insider_trade.company = stock_code
        except Exception:
            stock = Stock()
            stock_url = make_url('main', stock_code)
            stock_page = load_page(stock_url)
            stock_name = scrape_stock_name(stock_page)
            stock.name = stock_name
            stock.code = stock_code
            save_stock(stock)
            insider_trade.company = Stock().get_by_id(stock_code)

        insider_trade.insider = individual_code
        insider_trade.relation = element[2]
        trade_last_date = datetime.date(
            datetime.strptime(element[3], '%m/%d/%Y'))
        insider_trade.last_date = trade_last_date
        insider_trade.tran = element[5]
        insider_trade.owner_type = element[6]
        shares_traded = element[7].replace(',', '')
        if shares_traded == '':
            shares_traded = 0
        insider_trade.shares_traded = shares_traded
        last_price = element[8]
        if last_price == '':
            last_price = 0.0
        insider_trade.last_price = last_price
        shares_held = element[9].replace(',', '')
        if shares_held == '':
            shares_held = 0
        insider_trade.shares_held = shares_held
        try:
            insider_trade.save()
            logger.info(
                f'Trade object of {individual_code} on last date {element[3]} saved in db')
        except Exception as exception:
            print(exception)
            logger.error(f'{individual_code} is allready exist: {exception}')
            db.rollback()


def get_delta(value, price_type, ticker_code):
    query = (
        "SELECT MAX( select1.date ) as date1, date2 FROM ( \n"
        "SELECT t1.date, t1.{type}, \n"
        "MIN(t2.date) as date2 \n"
        "FROM price t1 \n"
        "INNER JOIN price t2 \n"
        "ON (t2.{type} >= t1.{type} + {value})\n"
        "AND t1.date < t2.date\n"
        "AND t1.stock_id = t2.stock_id\n"
        "WHERE t1.stock_id = '{ticker_code}'\n"
        "GROUP BY t1.id\n"
        "ORDER BY t1.date ) select1\n"
        "GROUP BY date2;").format(type=price_type, ticker_code=ticker_code, value=value)
    cursor = db.execute_sql(query)
    dates = [list(x) for x in cursor]
    print(dates)
    return dates

def get_analytics(date_from, date_to, ticker_code):
    trades = Price.select(
        Price.stock, Price.date,
        (Price.open - Price.close).alias("delta_open_close"),
        (Price.high - Price.low).alias("delta_high_low")).where(
        (Price.stock == ticker_code) &
        (Price.date.between(date_from, date_to)))
    return trades


def get_insider(insider_code):
    insider = Insider.get(Insider.code == insider_code)
    return insider


def get_ticker(ticker_code):
    stock = Stock.get(Stock.code == ticker_code.upper())
    return stock


def get_trades(ticker_code):
    trades = Trade.select().where(Trade.stock == ticker_code.upper()
                                  ).order_by(Trade.last_date.desc())
    return trades


def get_individual_trades(insider_code):
    individual_trades = IndividualInsiderTrades().select().where(
        IndividualInsiderTrades.insider == insider_code).order_by(IndividualInsiderTrades.last_date.desc())
    return individual_trades


def get_all_tickers():
    stock_list = Stock().select()
    return stock_list


def get_historical(ticker_code):
    prices = Price.select().where(
        Price.stock == ticker_code.upper()).order_by(Price.date.desc())
    return prices

# my_list = [['https://www.nasdaq.com/symbol/abm/insider-trades', 'ABM INDUSTRIES INC /DE/', 'Officer', '02/05/2018', 'Form 4', 'Acquisition (Non Open Market)', 'direct', '99', '34.96', '30,121'], ['https://www.nasdaq.com/symbol/abm/insider-trades', 'ABM INDUSTRIES INC /DE/', 'Officer', '01/15/2018', 'Form 4', 'Disposition (Non Open Market)', 'direct', '1,047', '38.87', '29,963'], ['https://www.nasdaq.com/symbol/abm/insider-trades', 'ABM INDUSTRIES INC /DE/', 'Officer', '01/10/2018', 'Form 4', 'Acquisition (Non Open Market)', 'direct', '3,223', '0', '31,055'], ['https://www.nasdaq.com/symbol/abm/insider-trades', 'ABM INDUSTRIES INC /DE/', 'Officer', '12/28/2017', 'Form 4', 'Acquisition (Non Open Market)', 'direct', '3,634', '0', '27,832'], ['https://www.nasdaq.com/symbol/abm/insider-trades', 'ABM INDUSTRIES INC /DE/', 'Officer', '11/06/2017', 'Form 4', 'Acquisition (Non Open Market)', 'direct', '78', '40.63', '24,198'], ['https://www.nasdaq.com/symbol/abm/insider-trades', 'ABM INDUSTRIES INC /DE/', 'Officer', '09/11/2017', 'Form 4', 'Acquisition (Non Open Market)', 'direct', '4,271', '0', '24,119'], ['https://www.nasdaq.com/symbol/abm/insider-trades', 'ABM INDUSTRIES INC /DE/', 'Officer', '09/08/2017', 'Form 4', 'Disposition (Non Open Market)', 'direct', '1,172', '40.21', '19,848'], ['https://www.nasdaq.com/symbol/abm/insider-trades', 'ABM INDUSTRIES INC /DE/', 'Officer', '09/06/2017', 'Form 4', 'Disposition (Non Open Market)', 'direct', '846', '44.14', '21,019'], ['https://www.nasdaq.com/symbol/abm/insider-trades', 'ABM INDUSTRIES INC /DE/', 'Officer', '08/07/2017', 'Form 4', 'Acquisition (Non Open Market)', 'direct', '76', '44.7', '21,865'], ['https://www.nasdaq.com/symbol/abm/insider-trades', 'ABM INDUSTRIES INC /DE/', 'Officer', '07/10/2017', 'Form 4', 'Automatic Sell', 'direct', '940', '40.92', '21,789'], [
#     'https://www.nasdaq.com/symbol/abm/insider-trades', 'ABM INDUSTRIES INC /DE/', 'Officer', '06/12/2017', 'Form 4', 'Acquisition (Non Open Market)', 'direct', '6,145', '0', '21,789'], ['https://www.nasdaq.com/symbol/abm/insider-trades', 'ABM INDUSTRIES INC/DE/', 'Officer', '06/09/2017', 'Form 4', 'Automatic Sell', 'direct', '950', '43.95', '15,644'], ['https://www.nasdaq.com/symbol/abm/insider-trades', 'ABM INDUSTRIES INC /DE/', 'Officer', '05/10/2017', 'Form 4', 'Automatic Sell', 'direct', '950', '43.1', '15,644'], ['https://www.nasdaq.com/symbol/abm/insider-trades', 'ABM INDUSTRIES INC /DE/', 'Officer', '05/01/2017', 'Form 4', 'Acquisition (Non Open Market)', 'direct', '54', '43.39', '15,644'], ['https://www.nasdaq.com/symbol/abm/insider-trades', 'ABM INDUSTRIES INC /DE/', 'Officer', '04/10/2017', 'Form 4', 'Automatic Sell', 'direct', '950', '41.88', '14,641'], ['https://www.nasdaq.com/symbol/abm/insider-trades', 'ABM INDUSTRIES INC /DE/', 'Officer', '03/10/2017', 'Form 4', 'Automatic Sell', 'direct', '950', '42.72', '15,591'], ['https://www.nasdaq.com/symbol/abm/insider-trades', 'ABM INDUSTRIES INC /DE/', 'Officer', '02/10/2017', 'Form 4', 'Automatic Sell', 'direct', '1,900', '40.28', '15,847'], ['https://www.nasdaq.com/symbol/abm/insider-trades', 'ABM INDUSTRIES INC /DE/', 'Officer', '02/06/2017', 'Form 4', 'Acquisition (Non Open Market)', 'direct', '59', '40.4', '17,751'], ['https://www.nasdaq.com/symbol/abm/insider-trades', 'ABM INDUSTRIES INC /DE/', 'Officer', '02/06/2017', 'Form 4', 'Disposition (Non Open Market)', 'direct', '5', '40.4', '17,747'], ['https://www.nasdaq.com/symbol/abm/insider-trades', 'ABM INDUSTRIES INC /DE/', 'Officer', '01/14/2017', 'Form 4', 'Disposition (Non Open Market)', 'direct', '1,099', '40.47', '17,692']]

# save_individual_trades(my_list, 'jacobsen-rene-989679')
