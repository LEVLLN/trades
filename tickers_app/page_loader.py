import requests
from bs4 import BeautifulSoup
from libs.log_writer import *

SITE_URL = 'https://www.nasdaq.com/symbol'

APP_NAME = 'scrape_data'
LOG_FILE_PATH = f'logs/{APP_NAME}.log'

def make_url(url_type, stock_code, page_num=1):
    url = ''
    if url_type == 'insider-trades':
        url = f'{SITE_URL}/{stock_code}/{url_type}?page={page_num}'
    elif url_type == 'historical':
        url = f'{SITE_URL}/{stock_code}/{url_type}'
    elif url_type == 'main':
        url = f'{SITE_URL}/{stock_code}/real-time'
    return url


def load_page(page_url):
    response = requests.get(page_url)
    page_text = response.text
    logger.info(f'The page on URL: {page_url} is loaded')
    return page_text

# save html page to file


def write_page_to_file(file, file_name):
    with open(f'{file_name}.html', 'w') as output_file:
        output_file.write(file)

logger = init_logger(LOG_FILE_PATH,APP_NAME)
