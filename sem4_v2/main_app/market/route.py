from flask import Blueprint

from access import external_required


blueprint_market = Blueprint('bp_market', __name__)


@blueprint_market.route('/', methods=['GET', 'POST'])
@external_required
def market() -> str:
    return 'Market app'
