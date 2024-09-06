import json
from typing import Callable

from flask import Flask, render_template, session

from auth.route import blueprint_auth
from report.route import blueprint_report
from query.route import blueprint_query
from market.route import blueprint_market
from access import login_required, group_required, external_required
from utils import get_config_dir


app: Flask = Flask(__name__)
app.secret_key = 'SuperKey'

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_query, url_prefix='/query')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_market, url_prefix='/market')

app.config['db_config'] = json.load(open(get_config_dir() / 'db.json'))
app.config['access_config'] = json.load(open(get_config_dir() / 'access.json'))


@app.route('/healthcheck')
def healthcheck() -> str:
    return 'OK'


@app.route('/')
@login_required
def menu_choice() -> str:
    return render_template('internal_user_menu.html' if session.get('user_group') else 'external_user_menu.html')


@app.route('/exit')
@login_required
def exit_func() -> str:
    session.clear()
    return render_template('exit.html')


def add_blueprint_access_handler(application: Flask, blueprint_names: list[str], handler: Callable) -> Flask:
    for view_func_name, view_func in application.view_functions.items():
        view_func_parts: list[str] = view_func_name.split('.')
        if len(view_func_parts) > 1:
            view_blueprint: str = view_func_parts[0]
            if view_blueprint in blueprint_names:
                view_func = handler(view_func)
                application.view_functions[view_func_name] = view_func
    return application


app = add_blueprint_access_handler(app, ['bp_query', 'bp_report'], group_required)
app = add_blueprint_access_handler(app, ['bp_market'], external_required)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
