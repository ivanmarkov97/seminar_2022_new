import os
from flask import Blueprint, render_template, current_app, request
from sql_provider import SQLProvider
from db_work import call_proc

blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_report.route('/', methods=['GET', 'POST'])
def start_report():
    rep_month = 9
    rep_year = 2022
    if_exists = 0
    res = call_proc(current_app.config['dbconfig'], 'product_report', rep_month, rep_year, if_exists)
    print('res=', res)
    return 'Done'
