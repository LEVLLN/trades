from data_utils import *
from multiprocessing.dummy import Pool as ThreadPool

TICKERS_FILE_NAME = 'tickers.txt'
MAX_PAGE_COUNT = 10
N_THEAD = 4


def get_tickers_from_file():
    tickers = []
    file = open(TICKERS_FILE_NAME, 'r')
    for line in file:
        tickers.append(line.replace('\n', ''))
    return tickers


def scrape_data(n_thead):
    """Parse processing in n theads for stock and historical where N thead count initialized in N_THEAD param"""
    tickers = get_tickers_from_file()
    pool = ThreadPool(n_thead)
    results_ticker = pool.map(download_stock_page, tickers)
    results_historical = pool.map(download_historical_page, tickers)
    pool.close()
    pool.join()
    """Parse processing without multi-theads"""
    create_trades(tickers)


def download_trades_page(ticker, page_num):
    url = page_loader.make_url('insider-trades', ticker, page_num)
    trade_page = page_loader.load_page(url)
    trades_list = scrape_insider_trades(trade_page)
    insider_code = save_insider(trades_list).code
    save_trades(trades_list, ticker, insider_code)


def create_trades(tickers):
    i = 1
    for ticker in tickers:
        while i <= MAX_PAGE_COUNT:
            download_trades_page(ticker, i)
            i = i + 1


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
    return ticker


def scrape_detail_data():
    insider_list = Insider().select()
    for insider in insider_list:
        print(insider.code)
        download_individual_trades_page(insider.code)


"""Running scrapping data"""
scrape_data(N_THEAD)
"""Running scrapping detail insiders data"""
scrape_detail_data()
