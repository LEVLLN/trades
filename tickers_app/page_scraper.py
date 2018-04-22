import page_loader
from bs4 import BeautifulSoup
from libs.log_writer import *

FIRST_HEADER_POSTFIX = 'Common Stock Real Time Stock Quotes'
SECOND_HEADER_POSTFIX = 'Capital Stock Real Time Stock Quotes'
HREF_PREFIX = 'https://www.nasdaq.com/quotes/insiders/'
TABLE_HEADER_INDEX = 0
APP_NAME = 'scrape_data'
LOG_FILE_PATH = f'logs/{APP_NAME}.log'


def scrape_insider_trades(page):
    try:
        soup = BeautifulSoup(page, 'html.parser')
        table_rows = soup.find(
            'table', {'class': 'certain-width'}).find_all('tr')
        # Deleting header of table from table rows
        table_rows.pop(TABLE_HEADER_INDEX)
        return scrape_table(table_rows)
    except Exception as scrape_exception:
        logger.info(
            f'Insider trades data can not be scrapped from page: {scrape_exception}')


def scrape_stock_name(page):
    try:
        soup = BeautifulSoup(page, 'html.parser')
        header = soup.find('h1').text
        stock_name = header.replace(FIRST_HEADER_POSTFIX, '').strip(' \t\n\r')
        stock_name = stock_name.replace(
            SECOND_HEADER_POSTFIX, '').strip(' \t\n\r')
        return stock_name
    except Exception as scrape_exception:
        logger.info(
            f'Stock name value can not be scrapped from page: {scrape_exception}')


def scrape_prices(page):
    try:
        soup = BeautifulSoup(page, 'html.parser')
        historical_container = soup.find('div', {'id': 'historicalContainer'})
        table = historical_container.find('table')
        table_body = table.find('tbody')
        table_rows = table_body.find_all('tr')
        table_rows.pop(TABLE_HEADER_INDEX)
        return scrape_table(table_rows)
    except Exception as scrape_exception:
        logger.info(
            f'Historical can not be scrapped from page : {scrape_exception}')


def scrape_individual_trades(page):
    try:
        soup = BeautifulSoup(page, 'html.parser')
        trades_container = soup.find('div', {'class': 'genTable'})
        table = trades_container.find('table')
        table_rows = table.find_all('tr')
        table_rows.pop(TABLE_HEADER_INDEX)
        return scrape_table(table_rows)
    except Exception as scrape_exception:
        logger.info(
            f'Insider can not be scrapped from page: {scrape_exception}')


def scrape_table(table_rows):
    try:
        row_list = []
        for row in table_rows:
            column_list = []
            for td in row.find_all('td'):
                if td.find('a', href=True):
                    href = td.find('a', href=True)['href']
                    insider_code = href.replace(
                        HREF_PREFIX, '').strip(' \t\n\r')
                    column_list.append(insider_code)
                column_list.append(td.text.strip())
            row_list.append(column_list)
        return row_list
    except Exception as scrape_exception:
        logger.info(
            f'Data from table of the page can not be scrapped: {scrape_exception}')


logger = init_logger(LOG_FILE_PATH, APP_NAME)

# url = page_loader.make_url(url_type='individual-trades',insider_code='jacobsen-rene-989679')
# page = page_loader.load_page(url)
# data = scrape_individual_trades(page)
# print(data)