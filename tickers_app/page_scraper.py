import page_loader
from bs4 import BeautifulSoup
from libs.log_writer import *

FIRST_HEADER_POSTFIX = 'Common Stock Real Time Stock Quotes'
SECOND_HEADER_POSTFIX = 'Capital Stock Real Time Stock Quotes'
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
        logger.info(f'Insider trades data from the page can not be scrapped: {scrape_exception}')


def scrape_stock_name(page):
    try:
        soup = BeautifulSoup(page, 'html.parser')
        header = soup.find('h1').text
        stock_name = header.replace(FIRST_HEADER_POSTFIX, '').strip(' \t\n\r')
        stock_name = stock_name.replace(
            SECOND_HEADER_POSTFIX, '').strip(' \t\n\r')
        return stock_name
    except Exception as scrape_exception:
        logger.info(f'Stock name value from the page can not be scrapped: {scrape_exception}')


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
        logger.info(f'Historical from the page can not be scrapped: {scrape_exception}')


def scrape_table(table_rows):
    try:
        element_list = []
        for row in table_rows:
            subelement_list = []
            for td in row.find_all('td'):
                subelement_list.append(td.text.strip())
            element_list.append(subelement_list)
        return element_list
    except Exception as scrape_exception:
        logger.info(f'Data from table of the page can not be scrapped: {scrape_exception}')


logger = init_logger(LOG_FILE_PATH, APP_NAME)
