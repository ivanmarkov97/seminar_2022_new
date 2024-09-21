from __future__ import annotations

from dataclasses import dataclass

from database.operations import select_dict


@dataclass
class AuthUserResponse:
    data: dict | None
    error_message: str
    status: bool


def find_user_with_form(web_form, db_config, provider):
    data = None
    status = False
    error_message = ''

    login = web_form.get('login')
    password = web_form.get('password')
    if login:
        user_info = find_user(provider, login, password, db_config)
        if user_info:
            status = True
            data = user_info[0]
        else:
            error_message = 'User not found'
    else:
        error_message = 'Login and password not provided'
    return AuthUserResponse(data=data, error_message=error_message, status=status)


def find_user(provider, login, password, db_config):
    sql_internal = provider.get('internal_user.sql', dict(login=login, password=password))
    sql_external = provider.get('external_user.sql', dict(login=login, password=password))

    for sql_query in [sql_internal, sql_external]:
        _user_info = select_dict(db_config, sql_query)

        if _user_info:
            return _user_info
    return None
