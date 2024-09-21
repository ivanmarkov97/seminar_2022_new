from __future__ import annotations

from dataclasses import dataclass

from database.operations import select_dict
from .transactions import TransactionProcessor, InvalidOrderDataException


@dataclass
class ItemsResponse:
    items: list | None
    status: bool
    error_message: str


@dataclass
class BasketResponse:
    basket: dict | None
    status: bool
    error_message: str


@dataclass
class TransactionResponse:
    order_id: str | None
    status: bool
    error_message: str


def get_all_products(db_config, provider):
    sql = provider.get('all_items.sql', {})
    items = select_dict(db_config, sql)
    return ItemsResponse(items=items, status=True, error_message='')


def add_product_to_basket(web_form, db_config, provider, basket):
    product_id = web_form.get('prod_id')
    sql = provider.get('item_description.sql', dict(product_id=product_id))
    items = select_dict(db_config, sql)
    if not items:
        return BasketResponse(basket=None, status=False, error_message='Product is missing')

    if product_id in basket:
        basket[product_id]['count'] = basket[product_id]['count'] + 1
    else:
        basket[product_id] = {
            'name': items[0]['name'],
            'price': items[0]['price'],
            'count': 1
        }
    return BasketResponse(basket=basket, status=True, error_message='')


def make_transaction(db_config, provider, basket, user_id):
    request_basket = []
    for product in basket:
        request_basket.append({
            'item_id': product,
            'price': basket[product]['price'],
            'count': basket[product]['count']
        })
    request_data = {'user_id': user_id, 'basket': request_basket}
    try:
        order_id = TransactionProcessor(provider, db_config).make_transaction(request_data)
        if order_id is None:
            return TransactionResponse(order_id=None, status=False, error_message='Error in transaction')
    except InvalidOrderDataException:
        return TransactionResponse(order_id=None, status=False, error_message='Wrong order structure')
    return TransactionResponse(order_id=order_id, status=True, error_message='')
