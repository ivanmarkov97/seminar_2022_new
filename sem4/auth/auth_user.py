from __future__ import annotations

from dataclasses import dataclass

from database.operations import select_dict


@dataclass
class AuthUserResponse:
    data: tuple | None
    schema: list | None
    error_message: str
    status: bool


def auth_user_with_form(web_form, session, db_config, provider):
    login = web_form.get('login')
    password = web_form.get('password')
    if login:
        user_info = define_user(provider, login, password, db_config)
        print('user_info', user_info)
        if user_info:
            user_dict = user_info[0]
            session['user_id'] = user_dict['user_id']
            session['user_group'] = user_dict['user_group']
            session.permanent = True
            return redirect(url_for('menu_choice'))
        else:
            return render_template('input_login.html', message='Пользователь не найден')
    return render_template('input_login.html', message='Повторите ввод')


def define_user(provider, login, password, db_config):
    sql_internal = provider.get('internal_user.sql', dict(login=login, password=password))
    sql_external = provider.get('external_user.sql', dict(login=login, password=password))

    for sql_query in [sql_internal, sql_external]:
        _user_info = select_dict(db_config, sql_query)

        if _user_info:
            return _user_info
    return None
