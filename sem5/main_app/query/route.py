import os

from flask import Blueprint, request, render_template, current_app

from database.operations import select
from database.sql_provider import SQLProvider
from access import group_required


blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/', methods=['GET', 'POST'])
@group_required
def queries():
    if request.method == 'GET':
        return render_template('product_form.html')
    else:
        input_product = request.form.get('product_name')
        if input_product:
            sql = provider.get('product.sql', dict(input_product=input_product))
            product_result, schema = select(current_app.config['db_config'], sql)
            return render_template('db_result.html', schema=schema, result=product_result)
        else:
            return "Repeat input"
