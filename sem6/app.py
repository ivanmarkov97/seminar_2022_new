import json
from typing import List, Callable

from flask import Flask, render_template, session

from auth.routes import blueprint_auth
from query.route import blueprint_query
from report.routes import blueprint_report
from market.routes import blueprint_market
from access import login_required, group_required, external_required


app: Flask = Flask(__name__)
app.secret_key = 'SuperKey'

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_query, url_prefix='/query')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_market, url_prefix='/market')

app.config['db_config'] = json.load(open('configs/db.json'))
app.config['access_config'] = json.load(open('configs/access.json'))


@app.route('/')
@login_required
def menu_choice() -> str:
    return render_template(
        'external_user_menu_kek_lol.html' if session.get('user_group') else 'internal_user_menu_kek_lol.html')


@app.route('/exit')
@login_required
def exit_func() -> str:
    session.clear()
    return render_template('exit.html')


def add_blueprint_access_handler(application: Flask, blueprint_names: List[str], handler: Callable) -> Flask:
    for view_func_name, view_func in application.view_functions.items():
        view_func_parts: list[str] = view_func_name.split('.')
        if len(view_func_parts) > 1:
            view_blueprint: str = view_func_parts[0]
            if view_blueprint in blueprint_names:
                view_func: Callable = handler(view_func)
                application.view_functions[view_func_name] = view_func
    return application


if __name__ == '__main__':
    app = add_blueprint_access_handler(app, ['blueprint_report'], group_required)
    app = add_blueprint_access_handler(app, ['blueprint_market'], external_required)
    app.run(host='127.0.0.1', port=5001)
