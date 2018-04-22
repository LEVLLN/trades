from flask import Blueprint, Flask, jsonify
from models import Stock, Price, Trade, Insider, IndividualInsiderTrades

model_api = Blueprint('account_api', __name__)


@model_api.route('/api/v1/tickers', methods=['GET'])
def get_all_tickers_json():
    stock = Stock.select()
    return jsonify(to_dicts(stock))


@model_api.route('/api/v1/tickers/<ticker_code>')
def ticker_historical(ticker_code):
    historical = Price.select().where(
        Price.stock == ticker_code.upper()).order_by(
            Price.date.desc()).dicts()
    return jsonify(to_dicts(historical))


def to_dicts(data):
    query = data.dicts()
    result_dicts = []
    for element in query:
        result_dicts.append(element)
    return result_dicts
