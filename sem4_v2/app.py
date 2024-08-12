import json

from flask import Flask, render_template, session

from auth.routes import blueprint_auth
from report.routes import blueprint_report
from query.route import blueprint_query
from access import login_required


app: Flask = Flask(__name__)
app.secret_key = 'SuperKey'

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_query, url_prefix='/query')
app.register_blueprint(blueprint_report, url_prefix='/report')

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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
