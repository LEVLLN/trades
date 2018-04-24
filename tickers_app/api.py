from flask import Blueprint, Flask, jsonify, request
from models import Stock, Price, Trade, Insider, IndividualInsiderTrades


model_api = Blueprint('account_api', __name__)


@model_api.route('/api/v1/tickers', methods=['GET'])
def get_all_tickers_json():
    stock = Stock.select().dicts()
    return jsonify(to_dicts(stock))


@model_api.route('/api/v1/<ticker_code>')
def ticker_historical(ticker_code):
    historical = Price.select().where(
        Price.stock == ticker_code.upper()).order_by(
            Price.date.desc()).dicts()
    return jsonify(to_dicts(historical))


@model_api.route('/api/v1/<ticker_code>/insider')
def get_ticker_trades(ticker_code):
    trades = Trade.select().where(Trade.stock == ticker_code.upper()
                                  ).order_by(Trade.last_date.desc()).dicts()
    return jsonify(to_dicts(trades))


@model_api.route('/api/v1/<ticker_code>/insider/<insider_code>')
def get_insider_trades(ticker_code, insider_code):
    individual_trades = IndividualInsiderTrades().select().where(
        IndividualInsiderTrades.insider == insider_code).order_by(IndividualInsiderTrades.last_date.desc()).dicts()
    return jsonify(to_dicts(individual_trades))


@model_api.route('/api/v1/<ticker_code>/analytics', methods=['GET'])
def analytics(ticker_code):
    date_from = request.args.get('date-from')
    date_to = request.args.get('date-to')
    stock = Stock.get(Stock.code == ticker_code.upper())
    trades = Price.select(Price.stock, Price.date,
                          (Price.open - Price.close).alias("delta_open_close"),
                          (Price.high - Price.low).alias("delta_high_low")).where(
        (Price.stock == ticker_code) &
        (Price.date.between(date_from, date_to))).dicts()
    return jsonify(to_dicts(trades))


def to_dicts(data):
    query = data
    result_dicts = []
    for element in query:
        result_dicts.append(element)
    return result_dicts
