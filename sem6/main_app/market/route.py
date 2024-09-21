import os
import json

from flask import Blueprint, render_template, request, session, redirect, url_for, current_app

from database.operations import select_dict
from database.sql_provider import SQLProvider
from cache.wrapper import fetch_from_cache
from utils import get_config_dir
from .market_operations import get_all_products, add_product_to_basket, make_transaction


blueprint_market = Blueprint('bp_market', __name__, template_folder='templates', static_folder='static')
sql_provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
cache_config = json.load(open(get_config_dir() / 'cache.json'))


@fetch_from_cache(cache_name='all_items_cache', cache_config=cache_config)
def cached_all_items_request():
    import time
    time.sleep(10)
    return get_all_products(current_app.config['db_config'], sql_provider)


def set_basket_in_session(basket):
    session['basket'] = basket
    session.permanent = True
    return redirect(url_for('bp_market.market_index_handler'))


def clear_basket_and_redirect(session):
    if 'basket' in session:
        session.pop('basket')
    return redirect(url_for('bp_market.market_index_handler'))


@blueprint_market.route('/', methods=['GET'])
def market_index_handler():
    return render_template(
        'market/index.html',
        items=get_all_products(current_app.config['db_config'], sql_provider).items,
        basket_items=session.get('basket', {})
    )


@blueprint_market.route('/', methods=['GET'])
def market_add_item_handler():
    response = add_product_to_basket(request.form, current_app.config['db_config'], sql_provider, session.get('basket', {}))
    return set_basket_in_session(response.basket) if response.status else render_template('market/item_missing.html')


@blueprint_market.route('/buy', methods=['GET'])
def market_transaction_handler():
    if not session.get('basket', {}):
        return redirect(url_for('bp_market.market_index'))
    response = make_transaction(current_app.config['db_config'], sql_provider, session['basket'], session['user_id'])
    return clear_basket_and_redirect(session) if response.status else response.error_message


@blueprint_market.route('/my-orders')
def user_orders():
    sql = f"SELECT * FROM orders WHERE user_id={session.get('user_id')}"
    return select_dict(current_app.config['db_config'], sql)


@blueprint_market.route('/clear-basket')
def clear_basket():
    return clear_basket_and_redirect(session)
