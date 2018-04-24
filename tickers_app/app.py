from flask import Flask, Response, jsonify
from flask import render_template, request
from models import Stock, Price, Trade, Insider, IndividualInsiderTrades
from api import model_api
from datetime import datetime

PORT = 8080
app = Flask(__name__)
app.register_blueprint(model_api)


@app.route('/')
def get_all_tickers():
    stock_list = Stock().select()
    return render_template('index.html', stocks=stock_list)


@app.route('/<ticker_code>')
def ticker_historical(ticker_code):
    stock = Stock().get(Stock.code == ticker_code.upper())
    historical = Price.select().where(
        Price.stock == ticker_code.upper()).order_by(Price.date.desc())
    return render_template('historical.html', prices=historical, ticker=stock)


@app.route('/<ticker_code>/insider')
def get_ticker_trades(ticker_code):
    stock = Stock.get(Stock.code == ticker_code.upper())
    trades = Trade.select().where(Trade.stock == ticker_code.upper()
                                  ).order_by(Trade.last_date.desc())
    return render_template('insider-trades.html', insider_trades=trades, ticker=stock)


@app.route('/<ticker_code>/insider/<insider_code>')
def get_insider_trades(ticker_code, insider_code):
    stock = Stock.get(Stock.code == ticker_code.upper())
    insider = Insider.get(Insider.code == insider_code)
    individual_trades = IndividualInsiderTrades().select().where(
        IndividualInsiderTrades.insider == insider_code).order_by(IndividualInsiderTrades.last_date.desc())
    return render_template(
        'individual-insider.html', individual_insider=insider, ticker=stock, trades=individual_trades)


@app.route('/<ticker_code>/analytics', methods=['GET'])
def analytics(ticker_code):
    date_from = request.args.get('date-from')
    date_to = request.args.get('date-to')
    stock = Stock.get(Stock.code == ticker_code.upper())
    trades = Price.select(Price.date,
                          (Price.open - Price.close).alias("delta_open_close"), 
                          (Price.high - Price.low).alias("delta_high_low")).where(
        (Price.stock == ticker_code) &
        (Price.date.between(date_from, date_to)))
    return render_template('analytics.html',result_prices=trades,ticker=stock)


if __name__ == "__main__":
    app.run(port=PORT)
