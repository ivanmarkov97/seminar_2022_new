from __future__ import annotations

import os
from base64 import b64encode
from typing import TYPE_CHECKING

import requests
from flask import Blueprint, request, render_template, session, redirect, url_for, current_app

from database.sql_provider import SQLProvider
from database.operations import select_dict

if TYPE_CHECKING:
    from werkzeug.wrappers.response import Response


blueprint_auth: Blueprint = Blueprint('bp_auth', __name__, template_folder='templates')
provider: SQLProvider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


def create_basic_auth_token(login: str, password: str) -> str:
    credentials_b64: str = b64encode(f'{login}:{password}'.encode('ascii')).decode('ascii')
    token = f'Basic {credentials_b64}'
    return token


def save_in_session_and_redirect(user_dict: dict) -> Response:
    session['user_id'] = user_dict['user_id']
    session['user_group'] = user_dict['user_group']
    session.permanent = True
    return redirect(url_for('menu_choice'))


@blueprint_auth.route('/', methods=['GET', 'POST'])
def start_auth() -> str | Response:
    if request.method == 'GET':
        return render_template('input_login.html', message='')
    else:
        login: str = request.form.get('login', '')
        password: str = request.form.get('password', '')
        is_internal: bool = True if request.form.get('is_internal') == 'on' else False

        if not login or not password:
            return render_template('input_login.html', message='Повторите ввод')

        if not is_internal:
            # make external API call
            response: requests.Response = requests.get(
                'http://127.0.0.1:5002/api/auth/find-user',
                headers={'Authorization': create_basic_auth_token(login, password)}
            )

            resp_json: dict = response.json()
            if resp_json['status'] == 200:
                return save_in_session_and_redirect(resp_json['user'])
        else:
            # find internal user
            sql: str = provider.get('user.sql', dict(login=login, password=password))
            user: list[dict] = select_dict(current_app.config['db_config'], sql)
            if user:
                return save_in_session_and_redirect(user[0])

        return render_template('input_login.html', message='Пользователь не найден')
