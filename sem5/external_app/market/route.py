import os

from flask import Blueprint, request, current_app, jsonify

from database.operations import select
from database.sql_provider import SQLProvider
from market.transaction import make_transaction


blueprint_market = Blueprint('bp_market', __name__)
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


def validate_order(order_data):
    if 'user_id' not in order_data:
        return False
    if 'basket' not in order_data:
        return False
    if not order_data['basket']:
        return False
    for order_item in order_data['basket']:
        if 'item_id' not in order_item:
            return False
        if 'price' not in order_item:
            return False
        if 'count' not in order_item:
            return False
    return True


@blueprint_market.route('/', methods=['GET'])
def market_all_items():
    db_config = current_app.config['db_config']
    sql = provider.get('all_items.sql')
    items = select(db_config, sql)
    return jsonify({'status': 200, 'items': items})


@blueprint_market.route('/<product_id>', methods=['GET'])
def market_all_items(product_id=None):
    db_config = current_app.config['db_config']
    sql = provider.get('item_description.sql', dict(product_id=product_id))
    items = select(db_config, sql)

    if not items:
        return jsonify({'status': 404, 'message': 'not found'})
    return jsonify({'status': 200, 'items': items})


@blueprint_market.route('/order', methods=['POST'])
def market_make_order():
    request_data = request.json

    if not validate_order(request_data):
        return jsonify({'status': 400, 'message': 'Bad request. Invalid order'})

    try:
        make_transaction(request_data)
        return jsonify({'status': 200})
    except Exception as e:
        return jsonify({'status': 502, 'message': f'Internal server error. {str(e)}'})
