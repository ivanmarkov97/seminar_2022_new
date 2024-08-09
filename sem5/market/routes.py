from __future__ import annotations

import os
from typing import TYPE_CHECKING

from flask import Blueprint, render_template, request, current_app, session, redirect, url_for

from database.operations import select
from database.sql_provider import SQLProvider

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
def market_index():
	db_config: dict = current_app.config['db_config']

	if request.method == 'GET':
		sql: str = provider.get('all_items.sql')
		items: list[dict] = select(db_config, sql)

		basket_items = session.get('basket', {})
		return render_template('market/index.html', items=items, basket_items=basket_items)
	else:
		prod_id: str | None = request.form['prod_id']
		sql: str = provider.get('item_description.sql', {'$product_id': prod_id})
		items: list[dict] = select(db_config, sql)

		items_description: list[dict] = [item for item in items if str(item['prod_id']) == str(prod_id)]

		if not items_description:
			return render_template('market/item_missing.html')

		item_description: dict = items_description[0]
		curr_basket: dict = session.get('basket', {})

		if prod_id in curr_basket:
			curr_basket[prod_id]['amount'] = curr_basket[prod_id]['amount'] + 1
		else:
			curr_basket[prod_id] = {
				'name': item_description['name'],
				'price': item_description['price'],
				'amount': 1
			}
		session['basket'] = curr_basket
		session.permanent = True

		return redirect(url_for('blueprint_market.market_index'))


@blueprint_market.route('/clear-basket')
def clear_basket() -> Response:
	if 'basket' in session:
		session.pop('basket')
	return redirect(url_for('blueprint_market.market_index'))
