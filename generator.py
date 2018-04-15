from data_utils import *


TICKERS_FILE_NAME = 'tickers.txt'


def get_tickers_from_file():
    tickers = []
    file = open(TICKERS_FILE_NAME, 'r')
    for line in file:
        tickers.append(line.replace('\n', ''))
    return tickers


def generate_data():
    tickers = get_tickers_from_file()
    for ticker in tickers:
        print(ticker)
        save_stock(ticker)


generate_data()
