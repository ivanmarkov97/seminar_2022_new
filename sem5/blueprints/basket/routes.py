import os

from flask import (
	Blueprint, session, render_template, current_app, request, redirect)

from database.connection import work_with_db
from database.sql_provider import SQLProvider
from access import AccessManager
from .utils import add_user_basket, clear_user_basket


basket_app = Blueprint('basket', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@basket_app.route('/', methods=['GET', 'POST'])
#@AccessManager.group_required
def list_orders():
	if request.method == 'GET':
		current_basket = session.get('basket', [])
		items = work_with_db(current_app.config['DB_CONFIG'], provider.get('order_list.sql'))
		print(items)
		return render_template('basket_order_list.html', items=items, basket=current_basket)
	else:
		action = request.form['action']
		item_id = request.form['item_id']
		print('item_id=', item_id)
		if action == 'Add':
			sql = provider.get('order_item.sql', prod_id=item_id)
			item = work_with_db(current_app.config['DB_CONFIG'], sql)
			if item:
				item = item[0]
			add_user_basket(item)
		return redirect('/order')


@basket_app.route('/clear')
#@AccessManager.group_required
def clear_basket():
	clear_user_basket()
	return redirect('/order')
