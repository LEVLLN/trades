import page_loader
from bs4 import BeautifulSoup
from models import URLParameter, Stock, Price, Trade

def scrape_trades_page(page):
    soup = BeautifulSoup(page, 'html.parser')
    table_rows = soup.find('table', {'class': 'certain-width'}).find_all('tr')
    # Deleting header of table from table rows
    table_rows.pop(0)
    for row in table_rows:
        for td in row.find_all('td'):
            print(f'{td.text}')
        print('---------------------------------------')
        
def scrape_stock_name(page):
    soup = BeautifulSoup(page,'html.parser')
    header = soup.find('h1').text
    stock_name = header.replace('Common Stock Historical Stock Prices','').strip(' \t\n\r')
    print(stock_name)

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
scrape_trades_page(historical_page)
