import os

from flask import (
	Blueprint, render_template,
	request, current_app,
	session, redirect, url_for
)

from database.operations import select
from database.sql_provider import SQLProvider


blueprint_market = Blueprint(
	'blueprint_market',
	__name__,
	template_folder='templates',
	static_folder='static'
)
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_market.route('/', methods=['GET', 'POST'])
def market_index():
	db_config = current_app.config['db_config']

	if request.method == 'GET':
		sql = provider.get('all_items.sql')
		items = select(db_config, sql)

		basket_items = session.get('basket', {})
		return render_template('market/index.html', items=items, basket_items=basket_items)
	else:
		item_id = request.form['item_id']
		sql = provider.get('all_items.sql')
		items = select(db_config, sql)

		item_description = [item for item in items if str(item['item_id']) == str(item_id)]

		if not item_description:
			return render_template('market/item_missing.html')

		item_description = item_description[0]
		curr_basket = session.get('basket', {})

		if item_id in curr_basket:
			curr_basket[item_id]['cnt'] = curr_basket[item_id]['cnt'] + 1
		else:
			curr_basket[item_id] = {
				'name': item_description['name'],
				'price': item_description['price'],
				'cnt': 1
			}
		session['basket'] = curr_basket
		session.permanent = True

		return redirect(url_for('blueprint_market.market_index'))


@blueprint_market.route('/clear-basket')
def clear_basket():
	if 'basket' in session:
		session.pop('basket')
	return redirect(url_for('blueprint_market.market_index'))
