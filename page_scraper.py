import page_loader
from bs4 import BeautifulSoup
from models import Stock, Price, Trade
from datetime import datetime

HEADER_POSTFIX = 'Common Stock Historical Stock Prices'
TABLE_HEADER_INDEX = 0


def scrape_insider_trades(page):
    soup = BeautifulSoup(page, 'html.parser')
    table_rows = soup.find('table', {'class': 'certain-width'}).find_all('tr')
    # Deleting header of table from table rows
    table_rows.pop(TABLE_HEADER_INDEX)
    return scrape_table(table_rows)


def scrape_stock_name(page):
    soup = BeautifulSoup(page, 'html.parser')
    header = soup.find('h1').text
    stock_name = header.replace(HEADER_POSTFIX, '').strip(' \t\n\r')
    return stock_name


def scrape_prices(page):
    soup = BeautifulSoup(page, 'html.parser')
    historical_container = soup.find('div', {'id': 'historicalContainer'})
    table = historical_container.find('table')
    table_body = table.find('tbody')
    table_rows = table_body.find_all('tr')
    table_rows.pop(TABLE_HEADER_INDEX)
    return scrape_table(table_rows)


def scrape_table(table_rows):
    element_list = []
    for row in table_rows:
        subelement_list = []
        for td in row.find_all('td'):
            if td.text.strip() != '':
                subelement_list.append(td.text.strip())
        element_list.append(subelement_list)
    return element_list

def save_prices(element_list,stock_code):
    for element in element_list:
       price = Price()
       price.stock = stock_code
       price.date = datetime.date(datetime.strptime(element[0],'%m/%d/%Y'))
       price.open = element[1]
       price.high = element[2]
       price.low = element[3]
       price.close = element[4]
       volume = element[5].replace(',','')
       price.volume = volume
       price.save()

def save_trades(element_list,stock_code):
    trades_list = []
    for element in element_list:
        stock = Stock()

# Scrape insider-trades page
# param = URLParameter()
# param.stock = 'aapl'
# param.page_num = 1
# param.url_type = 'insider-trades'
# url = page_loader.make_url(param)
# trades_page = page_loader.load_page(url)
# scrape_trades_page(trades_page)

url = page_loader.make_url('insider-trades','aapl')
print(url)
historical_page = page_loader.load_page(url)
el = scrape_insider_trades(historical_page)
# save_prices(el,'aapl')