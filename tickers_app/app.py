from flask import Flask, Response, jsonify
from flask import render_template, request
from models import Stock, Price, Trade, Insider, IndividualInsiderTrades
from api import model_api
from datetime import datetime
import data_utils

PORT = 8080
app = Flask(__name__)
app.register_blueprint(model_api)


@app.route('/')
def render_all_tickers():
    stock_list = data_utils.get_all_tickers()
    return render_template('index.html', stocks=stock_list)


@app.route('/<ticker_code>')
def render_ticker_historical(ticker_code):
    stock = data_utils.get_ticker(ticker_code)
    historical = data_utils.get_historical(ticker_code)
    return render_template('historical.html', prices=historical, ticker=stock)


@app.route('/<ticker_code>/insider')
def get_ticker_trades(ticker_code):
    stock = data_utils.get_ticker(ticker_code)
    trades = data_utils.get_trades(ticker_code)
    return render_template('insider-trades.html', insider_trades=trades, ticker=stock)


@app.route('/<ticker_code>/insider/<insider_code>')
def render_insider_trades(ticker_code, insider_code):
    stock = data_utils.get_ticker(ticker_code)
    insider = data_utils.get_insider(insider_code)
    individual_trades = data_utils.get_individual_trades(insider_code)
    return render_template(
        'individual-insider.html', individual_insider=insider, ticker=stock, trades=individual_trades)


@app.route('/<ticker_code>/analytics', methods=['GET'])
def render_analytics(ticker_code):
    date_from = request.args.get('date-from')
    date_to = request.args.get('date-to')
    stock = data_utils.get_ticker(ticker_code)
    trades = data_utils.get_analytics(date_from, date_to, ticker_code)
    return render_template('analytics.html', result_prices=trades, ticker=stock)


@app.route('/<ticker_code>/delta', methods=['GET'])
def render_delta(ticker_code):
    stock = data_utils.get_ticker(ticker_code)
    value = request.args.get('value')
    price_type = request.args.get('type')
    delta_list = data_utils.get_delta(value, price_type, ticker_code)
    return render_template('delta.html', value=value, dates=delta_list, ticker=stock)


@app.errorhandler(500)
def internal_error(error):
    return f"500 error: {error}"


if __name__ == "__main__":
    app.run(port=PORT)
