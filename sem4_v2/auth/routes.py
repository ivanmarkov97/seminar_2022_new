from __future__ import annotations

import os
import json
from typing import TYPE_CHECKING

import requests
from flask import Blueprint, request, render_template, session, redirect, url_for

from database.sql_provider import SQLProvider

if TYPE_CHECKING:
    from werkzeug.wrappers.response import Response


blueprint_auth: Blueprint = Blueprint('blueprint_auth', __name__, template_folder='templates')
provider: SQLProvider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


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

        link_path: str = 'internal' if is_internal else 'external'
        response: requests.Response = requests.post(
            f'http://127.0.0.1:5002/find-user/{link_path}',
            data=json.dumps({'login': login, 'password': password}),
            headers={'Content-Type': 'application/json'}
        )

        resp_json: dict = json.loads(response.text)
        if resp_json['status'] == 200:
            return save_in_session_and_redirect(resp_json['user'])

        return render_template('input_login.html', message='Пользователь не найден')
