import page_loader
from bs4 import BeautifulSoup

FIRST_HEADER_POSTFIX = 'Common Stock Real Time Stock Quotes'
SECOND_HEADER_POSTFIX = 'Capital Stock Real Time Stock Quotes'
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
    stock_name = header.replace(FIRST_HEADER_POSTFIX, '').strip(' \t\n\r')
    stock_name = stock_name.replace(SECOND_HEADER_POSTFIX,'').strip(' \t\n\r')
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
            subelement_list.append(td.text.strip())
        element_list.append(subelement_list)
    return element_list





# Scrape insider-trades page
# param = URLParameter()
# param.stock = 'aapl'
# param.page_num = 1
# param.url_type = 'insider-trades'
# url = page_loader.make_url(param)
# trades_page = page_loader.load_page(url)
# scrape_trades_page(trades_page)

# url = page_loader.make_url('insider-trades','aapl')
# print(url)
# historical_page = page_loader.load_page(url)
# el = scrape_insider_trades(historical_page)
# print(el)

# for stock_code in generator.get_tickers_from_file():
#     i = 1
#     stock = Stock()
#     stock.code = stock_code
#     url_stock = page_loader.make_url('main', stock_code)
#     page_stock = page_loader.load_page(url_stock)
#     stock.name = scrape_stock_name(page_stock)
#     stock.save()

#     while i <= 10:
#         url = page_loader.make_url('insider-trades', stock_code)
#         historical_page = page_loader.load_page(url)
#         el = scrape_insider_trades(historical_page)
#         save_trades(el, stock_code)
#         i = i+1
