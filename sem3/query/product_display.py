from __future__ import annotations

from dataclasses import dataclass

from database.operations import select


@dataclass
class ProductInfo:
    data: tuple | None
    schema: list | None
    error_message: str


def get_product(db_config, user_input_data, sql_provider):
    error_message = ''
    if 'product_name' not in user_input_data:
        error_message = '@product_name not found'
        return ProductInfo(data=None, schema=None, error_message=error_message)

    sql_query = sql_provider.get('product.sql', dict(input_product=user_input_data['product_name']))
    data, schema = select(db_config, sql_query)
    return ProductInfo(data=data, schema=schema, error_message=error_message)
