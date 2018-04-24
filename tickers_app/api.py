from flask import Blueprint, jsonify, request
import data_utils

MODEL_API = Blueprint('account_api', __name__)


@MODEL_API.route('/api/v1/', methods=['GET'])
def get_all_tickers_json():
    stock = data_utils.get_all_tickers().dicts()
    return jsonify(to_dicts(stock))


@MODEL_API.route('/api/v1/<ticker_code>')
def ticker_historical(ticker_code):
    historical = data_utils.get_historical(ticker_code).dicts()
    return jsonify(to_dicts(historical))


@MODEL_API.route('/api/v1/<ticker_code>/insider')
def get_ticker_trades(ticker_code):
    trades = data_utils.get_trades(ticker_code).dicts()
    return jsonify(to_dicts(trades))


@MODEL_API.route('/api/v1/<ticker_code>/insider/<insider_code>')
def get_insider_trades(insider_code):
    individual_trades = data_utils.get_individual_trades(insider_code).dicts()
    return jsonify(to_dicts(individual_trades))


@MODEL_API.route('/api/v1/<ticker_code>/analytics', methods=['GET'])
def get_analytics(ticker_code):
    date_from = request.args.get('date-from')
    date_to = request.args.get('date-to')
    trades = data_utils.get_analytics(date_from,date_to,ticker_code).dicts()
    return jsonify(to_dicts(trades))

@MODEL_API.route('/api/v1/<ticker_code>/delta', methods=['GET'])
def get_delta(ticker_code):
    value = request.args.get('value')
    price_type = request.args.get('type')
    deltas = data_utils.get_delta(value,price_type,ticker_code)
    for delta in deltas:
        delta.append(ticker_code)
    return jsonify(deltas)

def to_dicts(data):
    query = data
    result_dicts = []
    for element in query:
        result_dicts.append(element)
    return result_dicts
