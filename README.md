# trades
Trades app can scrapping insider-trades, historical and tickers data from [nasdaq web-site](http://www.nasdaq.com/symbols) and save this in DataBase.
Trades app is MVC web-app, you can get data about tickers, insider-trades and prices of tickers

### this is web-app with flask
```
pip install flask
```

### postgreSQL driver for connect to PostgreSQL
```
pip install psycopg2-binary
pip install psycopg2
```
### peewee library for ORM 
```
pip install peewee
```
### requests library for load pages by url
```
pip install requests
```
### beatifulSoup4 for scraping pages
```
pip install beautifulsoup4
```
### QUICK RUN
##### You need install Postgresql via this: [site](https://www.digitalocean.com/community/tutorials/postgresql-ubuntu-16-04-ru)
OR set the command in terminal:
```
sudo apt-get install sudo apt-get install postgresql postgresql-contrib
```
#### RUN and CREATE database
```
sudo -i -u postgres
CREATE DATABASE TRADES
psql -h localhost trades postgres
```
#### RUN parse pages and save data to db u need go to tickers_app and execute this:
``` 
python run_scrape_data.py
```
#### RUN web-app of tickers
```
python app.py
```