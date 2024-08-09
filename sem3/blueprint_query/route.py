from __future__ import annotations

import os
from typing import TYPE_CHECKING

from flask import Blueprint, request, render_template, current_app

from datbase.db_work import select
from database.sql_provider import SQLProvider

if TYPE_CHECKING:
    from werkzeug.wrappers.response import Response


blueprint_query: Blueprint = Blueprint('bp_query', __name__, template_folder='templates')
provider: SQLProvider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/queries', methods=['GET', 'POST'])
def queries() -> str | Response:
    if request.method == 'GET':
        return render_template('product_form.html')
    else:
        input_product: str | None = request.form.get('product_name')
        if input_product:
            sql: str = provider.get('product.sql', input_product=input_product)
            product_result, schema = select(current_app.config['dbconfig'], sql)
            return render_template('db_result.html', schema=schema, result=product_result)
        else:
            return "Repeat input"
