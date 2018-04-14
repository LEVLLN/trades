import requests
from bs4 import BeautifulSoup
from models import URLParameter


def make_url(param):
    url = ''
    if param.url_type == 'insider-trades':
        url = f'https://www.nasdaq.com/symbol/{param.stock}/{param.url_type}?page={param.page_num}'
    elif param.url_type == 'historical':
        url = f'https://www.nasdaq.com/symbol/{param.stock}/{param.url_type}'
    return url


def load_page(page_url):
    response = requests.get(page_url)
    page_text = response.text
    return page_text

# save html page to file


def write_page_to_file(file, file_name):
    with open(f'{file_name}.html', 'w') as output_file:
        output_file.write(file)