from __future__ import annotations

import os
from typing import Callable, TYPE_CHECKING

from flask import Blueprint, render_template, request, current_app, session, redirect, url_for

from database.db_work import select_dict
from database.sql_provider import SQLProvider
from cache.wrapper import fetch_from_cache

if TYPE_CHECKING:
	from werkzeug.wrappers.response import Response


blueprint_market: Blueprint = Blueprint(
	'blueprint_market',
	__name__,
	template_folder='templates',
	static_folder='static'
)
provider: SQLProvider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_market.route('/', methods=['GET', 'POST'])
def market_index() -> str | Response:
	db_config: dict = current_app.config['db_config']
	cache_config: dict = current_app.config['cache_config']
	cached_func: Callable = fetch_from_cache('all_items_cached', cache_config)(select_dict)

	if request.method == 'GET':
		sql: str = provider.get('all_items.sql')
		items: list[dict] = cached_func(db_config, sql)

		basket_items: dict = session.get('basket', {})
		return render_template('market/index.html', items=items, basket_items=basket_items)
	else:
		prod_id: str = request.form['prod_id']
		sql: str = provider.get('all_items.sql')
		items: list[dict] = cached_func(db_config, sql)

		item_descriptions: list[dict] = [item for item in items if str(item['prod_id']) == str(prod_id)]

		if not item_descriptions:
			return render_template('market/item_missing.html')

		item_description: dict = item_descriptions[0]
		curr_basket: dict = session.get('basket', {})

		if prod_id in curr_basket:
			curr_basket[prod_id]['cnt'] = curr_basket[prod_id]['cnt'] + 1
		else:
			curr_basket[prod_id] = {
				'name': item_description['name'],
				'price': item_description['price'],
				'cnt': 1
			}
		session['basket'] = curr_basket
		session.permanent = True

		return redirect(url_for('blueprint_market.market_index'))


@blueprint_market.route('/clear-basket')
def clear_basket() -> Response:
	if 'basket' in session:
		session.pop('basket')
	return redirect(url_for('blueprint_market.market_index'))
