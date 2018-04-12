import page_loader
from bs4 import BeautifulSoup
from models import URLParameter, Stock, Price, Trade

HEADER_POSTFIX = 'Common Stock Historical Stock Prices'
TABLE_HEADER_INDEX = 0


def scrape_insider_trades(page):
    soup = BeautifulSoup(page, 'html.parser')
    table_rows = soup.find('table', {'class': 'certain-width'}).find_all('tr')
    # Deleting header of table from table rows
    table_rows.pop(TABLE_HEADER_INDEX)
    scrape_table(table_rows)


def scrape_stock_name(page):
    soup = BeautifulSoup(page, 'html.parser')
    header = soup.find('h1').text
    stock_name = header.replace(HEADER_POSTFIX, '').strip(' \t\n\r')
    return stock_name

def scrape_prices(page):
    soup = BeautifulSoup(page, 'html.parser')
    historical_container = soup.find('div',{'id':'historicalContainer'})
    table = historical_container.find('table')
    table_body = table.find('tbody')
    table_rows = table_body.find_all('tr')
    scrape_table(table_rows)

def scrape_table(table_rows):
    for row in table_rows:
        for td in row.find_all('td'):
            print(f'{td.text.strip()}')
        print('---------------------------------------')
# Scrape insider-trades page
# param = URLParameter()
# param.stock = 'aapl'
# param.page_num = 1
# param.url_type = 'insider-trades'
# url = page_loader.make_url(param)
# trades_page = page_loader.load_page(url)
# scrape_trades_page(trades_page)


param = URLParameter()
param.stock = 'aapl'
param.page_num = 1
param.url_type = 'insider-trades'
url = page_loader.make_url(param)
historical_page = page_loader.load_page(url)
# scrape_stock_name(historical_page)
scrape_insider_trades(historical_page)
