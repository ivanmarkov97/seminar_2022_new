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
            if user_type:
                session['user_type'] = user_type
                session['user_identity'] = identity[0][0]
            else:
                return render_template('input_login.html', message='Пользователь не найден')
        else:
            return render_template('input_login.html', message='Повторите ввод')

    return redirect(url_for('menu_choice'))


@blueprint_auth.route('/define_user', methods=['GET', 'POST'])
def define_user(login, password):
    sql_internal = provider.get('internal_user.sql', login=login, password= password)
    sql_external = provider.get('external_user.sql', login=login, password=password)
    user_type = None
    identity, schema = work_with_db(current_app.config['dbconfig'], sql_internal)
    if identity:
        user_type = 1
    else:
        identity, schema = work_with_db(current_app.config['dbconfig'], sql_external)
        if identity:
            user_type = 2
    return user_type, identity






