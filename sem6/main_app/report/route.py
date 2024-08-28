from flask import Blueprint, current_app

from database.operations import call_proc
from access import group_required


blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')


@blueprint_report.route('/', methods=['GET', 'POST'])
@group_required
def start_report() -> str:
    rep_month: int = 9
    rep_year: int = 2022
    if_exists: int = 0
    res = call_proc(current_app.config['db_config'], 'product_report', rep_month, rep_year, if_exists)
    if res:
        return str(res)
    return 'Не удалось вызвать процедуру'
