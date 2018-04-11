import requests
from bs4 import BeautifulSoup
from parameter import Parameter


def make_url(param):
    url = ''
    if param.url_type == 'insider-trades':
        url = f'https://www.nasdaq.com/symbol/{param.stock}/{param.url_type}?page={param.page_num}'
    elif param.url_type == 'historical':
        url = 'historical'
    return url


def load_page(page_url):
    response = requests.get(page_url)
    page_text = response.text
    return page_text

# save html page to file


def write_page_to_file(file):
    with open('test.html', 'w') as output_file:
        output_file.write(file)


# scraping page with beautifulsoup
# soup = BeautifulSoup(r.text,"html.parser")
# trade_table = soup.find('table',{'class':'certain-width'})
# tbody = trade_table.find_all('tr')
# for td in tbody[1]:
#     print(f"{td} table")

# class Trade(object):
#     relation = ''
#     last_date = ''
#     transaction_type = ''
#     owner_type = ''
#     shares_traded = ''
#     last_price = ''
#     shares_held = ''

# def scrape_page(page):
#     soup = BeautifulSoup(page,'html.parser')
#     table_rows = soup.find('table',{'class':'certain-width'}).find_all('tr')
# # Deleting header of table from table rows
#     table_rows.pop(0)

#     for row in table_rows:
#         for td in row.find_all('td'):
#             print(f'{td.text} -f')
#         print('------------------------')

# scrape_page(load_page('aapl',1))
