import os
import json
from pathlib import Path

from flask import Blueprint, request, current_app, jsonify

from database.operations import select_dict, DBContextManager
from database.sql_provider import SQLProvider
from .transactions import TransactionProcessor, InvalidOrderDataException
from cache.wrapper import fetch_from_cache


blueprint_market = Blueprint('bp_market', __name__)
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
cache_config = json.load(open(Path('.').resolve() / 'configs/cache.json'))


@fetch_from_cache(cache_name='all_items_cache', cache_config=cache_config)
def cached_all_items_select():
    db_config = current_app.config['db_config']
    sql = provider.get('all_items.sql', {})
    items = select_dict(db_config, sql)
    return items


@blueprint_market.route('/', methods=['GET'])
def market_all_items():
    items = cached_all_items_select()
    return jsonify({'status': 200, 'items': items})


@blueprint_market.route('/<product_id>', methods=['GET'])
def market_show_item(product_id=None):
    db_config = current_app.config['db_config']
    sql = provider.get('item_description.sql', dict(product_id=product_id))
    items = select_dict(db_config, sql)

    if not items:
        return jsonify({'status': 404, 'message': 'not found'})
    return jsonify({'status': 200, 'items': items})


@blueprint_market.route('/order', methods=['POST'])
def market_make_order():
    try:
        order_id = TransactionProcessor(provider, current_app.config['db_config']).make_transaction(request.json)
        if order_id is None:
            raise ValueError('Could not create transaction due DB error.')
        return jsonify({'status': 200, 'order_id': order_id})

    except InvalidOrderDataException:
        return jsonify({'status': 400, 'message': 'Bad request. Invalid order'})
    except Exception as e:
        return jsonify({'status': 502, 'message': f'Internal server error. {str(e)}'})


@blueprint_market.route('/<user_id>/orders')
def user_orders(user_id=None):
    sql = f"SELECT * FROM orders WHERE user_id={user_id}"
    orders = select_dict(current_app.config['db_config'], sql)
    return jsonify({'status': 200, 'orders': orders})
