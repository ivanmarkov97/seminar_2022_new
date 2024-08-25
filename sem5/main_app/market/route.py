import json

import requests
from flask import Blueprint, render_template, request, session, redirect, url_for

from cache.wrapper import fetch_from_cache
from utils import get_config_dir


blueprint_market = Blueprint('bp_market', __name__, template_folder='templates', static_folder='static')
cache_config = json.load(open(get_config_dir() / 'cache.json'))

MARKET_SERVICE_URL = 'http://127.0.0.1:5002/api/market'


@fetch_from_cache(cache_name='all_items_cache', cache_config=cache_config)
def cached_all_items_request():
    import time
    time.sleep(10)
    return requests.get(MARKET_SERVICE_URL, timeout=10).json()


@blueprint_market.route('/', methods=['GET', 'POST'])
def market_index():
    if request.method == 'GET':
        all_products_response = cached_all_items_request()
        if all_products_response['status'] == 200:
            basket_items = session.get('basket', {})
            return render_template(
                'market/index.html',
                items=all_products_response['items'],
                basket_items=basket_items
            )
    else:
        prod_id = request.form['prod_id']
        product_response = requests.get(f"{MARKET_SERVICE_URL}/{prod_id}", timeout=10)
        if product_response.json()['status'] != 200:
            return render_template('market/item_missing.html')

        item_description = product_response.json()['items'][0]
        curr_basket = session.get('basket', {})
        if prod_id in curr_basket:
            curr_basket[prod_id]['count'] = curr_basket[prod_id]['count'] + 1
        else:
            curr_basket[prod_id] = {
                'name': item_description['name'],
                'price': item_description['price'],
                'count': 1
            }
        session['basket'] = curr_basket
        session.permanent = True
        return redirect(url_for('bp_market.market_index'))


@blueprint_market.route('/buy', methods=['GET'])
def market_transaction():
    curr_basket = session.get('basket', {})
    if not curr_basket:
        return redirect(url_for('bp_market.market_index'))
    user_id = session['user_id']
    request_basket = []
    for product in curr_basket:
        request_basket.append({
            'item_id': product,
            'price': curr_basket[product]['price'],
            'count': curr_basket[product]['count']
        })
    request_data = {'user_id': user_id, 'basket': request_basket}
    response = requests.post(f'{MARKET_SERVICE_URL}/order', json=request_data, timeout=10)
    if response.json()['status'] != 200:
        return response.json()['message']
    session.pop('basket')
    order_id = response.json()['order_id']
    return f'Создан заказ {order_id}'


@blueprint_market.route('/my-orders')
def user_orders():
    user_id = session.get('user_id')
    response = requests.get(f'{MARKET_SERVICE_URL}/{user_id}/orders')
    if response.json()['status'] != 200:
        return 'Error during client orders search'
    return response.json()['orders']


@blueprint_market.route('/clear-basket')
def clear_basket():
    if 'basket' in session:
        session.pop('basket')
    return redirect(url_for('bp_market.market_index'))
