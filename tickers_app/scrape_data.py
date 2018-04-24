from data_utils import *
from concurrent.futures import ThreadPoolExecutor

TICKERS_FILE_NAME = 'tickers.txt'
MAX_PAGE_COUNT = 10


def get_tickers_from_file():
    tickers = []
    file = open(TICKERS_FILE_NAME, 'r')
    for line in file:
        tickers.append(line.replace('\n', ''))
    return tickers


def scrape_data():
    tickers = get_tickers_from_file()
    for ticker in tickers:
        download_stock_page(ticker)
        download_historical_page(ticker)
        i = 1
        while i <= MAX_PAGE_COUNT:
            download_trades_page(ticker, i)
            i = i + 1


def download_trades_page(ticker, page_num):
    url = page_loader.make_url('insider-trades', ticker, page_num)
    trade_page = page_loader.load_page(url)
    trades_list = scrape_insider_trades(trade_page)
    insider_code = save_insider(trades_list).code
    save_trades(trades_list, ticker, insider_code)


def download_historical_page(ticker):
    url = page_loader.make_url('historical', ticker)
    trade_page = page_loader.load_page(url)
    trades_list = scrape_prices(trade_page)
    save_prices(trades_list, ticker)


def download_individual_trades_page(insider, page_number=1):
    url = page_loader.make_url(
        'individual-trades', insider_code=insider, page_num=page_number)
    print(url)
    page = page_loader.load_page(url)
    trades_list = scrape_individual_trades(page)
    save_individual_trades(trades_list, insider)


def download_stock_page(ticker):
    stock = Stock()
    stock_url = make_url('main', ticker)
    stock_page = load_page(stock_url)
    stock_name = scrape_stock_name(stock_page)
    stock.name = stock_name
    stock.code = ticker
    save_stock(stock)


def scrape_detail_data():
    insider_list = Insider().select()
    for insider in insider_list:
        print(insider.code)
        download_individual_trades_page(insider.code)

# scrape_data()


# scrape_detail_data()


# def task_queue(task, iterator, concurrency=10):
#     def submit():
#         try:
#            obj = next(iterator)
#         except StopIteration:
#             return
#     stats['delayed'] += 1
#     future = executor.submit(task, obj)
#     future.add_done_callback(upload_done)
#     def upload_done(future):
#        submit()
#        stats['delayed'] -= 1
#        stats['done'] += 1
# generate_data()
