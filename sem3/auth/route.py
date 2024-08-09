from __future__ import annotations

import os
from typing import TYPE_CHECKING

from flask import Blueprint, request, render_template, current_app, session, redirect, url_for

from database.db_work import select_dict
from database.sql_provider import SQLProvider

if TYPE_CHECKING:
    from werkzeug.wrappers.response import Response


blueprint_auth: Blueprint = Blueprint('blueprint_auth', __name__, template_folder='templates')
provider: SQLProvider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_auth.route('/', methods=['GET', 'POST'])
def start_auth() -> str | Response:
    if request.method == 'GET':
        return render_template('input_login.html', message='')
    else:
        login: str | None = request.form.get('login')
        password: str | None = request.form.get('password')
        if login:
            user_info: list[dict] = define_user(login, password)
            if user_info:
                user_dict: dict = user_info[0]
                session['user_id'] = user_dict['user_id']
                session['user_group'] = user_dict['user_group']
                session.permanent = True
                return redirect(url_for('menu_choice'))
            else:
                return render_template('input_login.html', message='Пользователь не найден')
        return render_template('input_login.html', message='Повторите ввод')


def define_user(login: str, password: str) -> list[dict] | None:
    sql_internal: str = provider.get('internal_user.sql', login=login, password=password)
    sql_external: str = provider.get('external_user.sql', login=login, password=password)

    for sql_query in [sql_internal, sql_external]:
        _user_info: list[dict] = select_dict(current_app.config['db_config'], sql_query)

        if _user_info:
            return _user_info
    return None
