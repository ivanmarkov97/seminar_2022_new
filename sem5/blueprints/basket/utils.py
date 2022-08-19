from flask import session


def add_user_basket(item):
	basket = session.get('basket', [])
	basket.append(item)
	session['basket'] = basket


def remove_item_by_id(item_id):
	basket = session.get('basket', [])
	basket = [item for item in basket if str(item['item_id']) != item_id]
	session['basket'] = basket


def clear_user_basket():
	if 'basket' in session:
		session.pop('basket')
