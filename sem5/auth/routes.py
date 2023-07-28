from base64 import b64encode

import requests
from flask import (
    Blueprint, request,
    render_template, current_app,
    session, redirect, url_for
)


blueprint_auth = Blueprint('blueprint_auth', __name__, template_folder='templates')

def encode_user_credentials(login, password):
    token = b64encode(f'{login}:{password}'.encode('utf-8')).decode('utf-8')
    return f'Basic {token}'


@blueprint_auth.route('/', methods=['GET', 'POST'])
def start_auth():
    if request.method == 'GET':
        return render_template('input_login.html', message='')
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        if login:
            user_token = encode_user_credentials(login, password)
            headers = {'Authorization': user_token}
            user_info_response = requests.get('http://127.0.0.1:5002/api/v1/user', headers=headers)
            if user_info_response.status_code == 200:
                user_info = user_info_response.json()
                session['user_id'] = user_info['user_id']
                session['user_group'] = user_info['user_group']
                session.permanent = True
                return redirect(url_for('menu_choice'))
            else:
                return render_template('input_login.html', message='Пользователь не найден')
        return render_template('input_login.html', message='Повторите ввод')
