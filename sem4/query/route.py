import os

from flask import Blueprint, request, render_template, current_app

from database.sql_provider import SQLProvider
from .product_display import get_product


blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/', methods=['GET'])
def all_products_handler():
    return render_template('product_form.html')


@blueprint_query.route('/', methods=['POST'])
def product_description_handler():
    product_info = get_product(current_app.config['db_config'], request.form, provider)
    return render_template('db_result.html', context=product_info)

