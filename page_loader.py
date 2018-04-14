import requests
from bs4 import BeautifulSoup


def make_url(url_type,stock_code,page_num=1):
    url = ''
    if url_type == 'insider-trades':
        url = f'https://www.nasdaq.com/symbol/{stock_code}/{url_type}?page={page_num}'
    elif url_type == 'historical':
        url = f'https://www.nasdaq.com/symbol/{stock_code}/{url_type}'
    return url


def load_page(page_url):
    response = requests.get(page_url)
    page_text = response.text
    return page_text

# save html page to file


def write_page_to_file(file, file_name):
    with open(f'{file_name}.html', 'w') as output_file:
        output_file.write(file)