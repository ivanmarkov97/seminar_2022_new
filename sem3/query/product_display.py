from __future__ import annotations

from dataclasses import dataclass

from database.operations import select_dict


@dataclass
class ProductInfoResponse:
    data: list | None
    error_message: str
    status: bool


def get_product(db_config, user_input_data, sql_provider):
    error_message = ''
    if 'product_name' not in user_input_data:
        error_message = '@product_name not found'
        return ProductInfoResponse(data=None, error_message=error_message, status=False)

    sql_query = sql_provider.get('product.sql', dict(input_product=user_input_data['product_name']))
    data = select_dict(db_config, sql_query)
    return ProductInfoResponse(data=data, error_message=error_message, status=True)
