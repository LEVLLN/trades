from flask import Flask
from flask import render_template
from models import Stock, Price, Trade


PORT = 8080
app = Flask(__name__)

@app.route('/')
def main():
    stock_list = Stock().select()
    return render_template('index.html', stocks=stock_list)


@app.route('/<ticker_code>')
def ticker_historical(ticker_code):
    stock = Stock().get(Stock.code == ticker_code.upper())
    historical = Price.select().where(Price.stock == ticker_code.upper())
    return render_template('historical.html', prices=historical, ticker=stock)


if __name__ == "__main__":
    app.run(port=PORT)
