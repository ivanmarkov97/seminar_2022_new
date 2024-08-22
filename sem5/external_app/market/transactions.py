from datetime import datetime

from flask import current_app

from database.connection import DBContextManager


def create_order_sql(data, sql_provider):
    user_id = data['user_id']
    order_dt = datetime.now()

    order_total_price = 0
    order_total_items = 0
    for order_item in data['basket']:
        order_total_items += order_item['count']
        order_total_price += order_item['count'] * order_item['price']

    return sql_provider.get(
        'order.sql',
        dict(
            user_id=user_id,
            order_dt=order_dt,
            order_total_price=order_total_price,
            order_total_items=order_total_items
        )
    )


def create_order_details_sql(data, sql_provider, order_id):
    sqls = []
    for order_item in data['basket']:
        prod_id = order_item['item_id']
        prod_price = order_item['price']
        prod_count = order_item['count']
        sql = sql_provider.get(
            'order_detail.sql',
            dict(
                order_id=order_id,
                prod_id=prod_id,
                prod_price=prod_price,
                prod_count=prod_count
            )
        )
        sqls.append(sql)
    return sqls


def make_transaction(data, sql_provider):

    with DBContextManager(current_app.config['db_config'], as_transaction=True) as cursor:
        if cursor is None:
            raise ValueError('Cursor is None')

        order_sql = create_order_sql(data, sql_provider)
        order_id = cursor.execute(order_sql)

        order_details_sqls = create_order_details_sql(data, sql_provider, order_id)
        for order_detail_sql in order_details_sqls:
            cursor.execute(order_detail_sql)
