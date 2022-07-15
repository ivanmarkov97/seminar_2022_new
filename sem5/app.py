import json
from typing import List, Callable

from flask import Flask, render_template, session
from auth.routes import blueprint_auth
from report.routes import blueprint_report
from market.routes import blueprint_market
from access import login_required, group_required, external_required


app = Flask(__name__)
app.secret_key = 'SuperKey'

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_market, url_prefix='/market')

app.config['db_config'] = json.load(open('configs/db.json'))
app.config['access_config'] = json.load(open('configs/access.json'))


@app.route('/')
@login_required
def menu_choice():
    if session.get('user_group', None):
        return render_template('internal_user_menu.html')
    return render_template('external_user_menu.html')


@app.route('/exit')
@login_required
def exit_func():
    session.clear()
    return render_template('exit.html')


def add_blueprint_access_handler(app: Flask, blueprint_names: List[str], handler: Callable) -> Flask:
    for view_func_name, view_func in app.view_functions.items():
        view_func_parts = view_func_name.split('.')
        if len(view_func_parts) > 1:
            view_blueprint = view_func_parts[0]
            if view_blueprint in blueprint_names:
                view_func = handler(view_func)
                app.view_functions[view_func_name] = view_func
    return app


if __name__ == '__main__':
    app = add_blueprint_access_handler(app, ['blueprint_report'], group_required)
    app = add_blueprint_access_handler(app, ['blueprint_market'], external_required)
    app.run(host='127.0.0.1', port=5001)
