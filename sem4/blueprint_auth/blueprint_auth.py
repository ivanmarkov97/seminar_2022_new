import os

from flask import Blueprint, request, render_template, current_app, session
from flask import redirect, url_for
from db_work import work_with_db
from sql_provider import SQLProvider


blueprint_auth = Blueprint('blueprint_auth', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))
print('provider=',provider)


@blueprint_auth.route('/auth', methods=['GET','POST'])
def start_auth():
    if request.method == 'GET':
        return render_template('input_login.html', message='')
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        if login:
            user_type, identity = define_user(login, password)
        else:
            return render_template('input_login,html', message='Повторите ввод')
    if user_type == 1:
        session['user_type'] = 'internal'
        session['user_group'] = identity[0][0]
    elif user_type == 2:
        session['user_type'] = 'external'
        session['user_id'] = identity[0][0]
    return redirect(url_for('menu_choice'))


@blueprint_auth.route('/define_user', methods=['GET', 'POST'])
def define_user(login, password):
    sql_internal = provider.get('internal_user.sql', login=login, password= password)
    sql_external = provider.get('external_user.sql', login=login, password=password)
    group, schema = work_with_db(current_app.config['dbconfig'], sql_internal)
    if group:
        user_type = 1
        return user_type, group
    else:
        user_id, schema = work_with_db(current_app.config['dbconfig'], sql_external)
        if user_id:
            user_type = 2
            return user_type, user_id






