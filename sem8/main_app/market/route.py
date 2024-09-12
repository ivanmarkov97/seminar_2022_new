from __future__ import annotations

import os
import json
from typing import TYPE_CHECKING

from flask import Blueprint, render_template, request, session, redirect, url_for, current_app

from database.operations import select_dict
from database.sql_provider import SQLProvider
from cache.wrapper import fetch_from_cache
from utils import get_config_dir
from .transactions import TransactionProcessor, InvalidOrderDataException

if TYPE_CHECKING:
    from werkzeug.wrappers.response import Response

blueprint_market: Blueprint = Blueprint('bp_market', __name__, template_folder='templates', static_folder='static')
sql_provider: SQLProvider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
cache_config: dict = json.load(open(get_config_dir() / 'cache.json'))


@fetch_from_cache(cache_name='all_items_cache', cache_config=cache_config)
def cached_all_items_request() -> list[dict]:
    import time
    time.sleep(10)
    db_config = current_app.config['db_config']
    sql = sql_provider.get('all_items.sql', {})
    items = select_dict(db_config, sql)
    return items


@blueprint_market.route('/', methods=['GET', 'POST'])
def market_index() -> str | Response:
    if request.method == 'GET':
        items = cached_all_items_request()
        basket_items = session.get('basket', {})
        return render_template(
            'market/index.html',
            items=items,
            basket_items=basket_items
        )
    else:
        db_config = current_app.config['db_config']
        prod_id = request.form['prod_id']
        sql = sql_provider.get('item_description.sql', dict(product_id=prod_id))
        items = select_dict(db_config, sql)
        if not items:
            return render_template('market/item_missing.html')

        item_description = items[0]
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
def market_transaction() -> str | Response:
    curr_basket: dict = session.get('basket', {})
    if not curr_basket:
        return redirect(url_for('bp_market.market_index'))
    user_id: str = session['user_id']
    request_basket: list[dict] = []
    for product in curr_basket:
        request_basket.append({
            'item_id': product,
            'price': curr_basket[product]['price'],
            'count': curr_basket[product]['count']
        })
    request_data: dict = {'user_id': user_id, 'basket': request_basket}

    try:
        order_id: str | None = TransactionProcessor(
            sql_provider,
            current_app.config['db_config']
        ).make_transaction(request_data)
        if order_id is None:
            return 'Ошибка в транзакции'
    except InvalidOrderDataException:
        return 'Неверная структура заказа'

    session.pop('basket')
    return f'Создан заказ {order_id}'


@blueprint_market.route('/my-orders')
def user_orders() -> list[dict]:
    user_id: str | None = session.get('user_id')
    sql: str = f"SELECT * FROM orders WHERE user_id={user_id}"
    orders: list[dict] = select_dict(current_app.config['db_config'], sql)
    return orders


@blueprint_market.route('/clear-basket')
def clear_basket() -> Response:
    if 'basket' in session:
        session.pop('basket')
    return redirect(url_for('bp_market.market_index'))
