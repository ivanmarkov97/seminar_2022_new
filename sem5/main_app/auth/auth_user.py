from __future__ import annotations

from base64 import b64encode
from dataclasses import dataclass

import requests

from database.operations import select_dict


@dataclass
class AuthUserResponse:
    data: dict | None
    error_message: str
    status: bool


def create_basic_auth_token(login, password):
    credentials_b64 = b64encode(f'{login}:{password}'.encode('ascii')).decode('ascii')
    token = f'Basic {credentials_b64}'
    return token


def find_user_with_form(web_form, db_config, provider):
    login = web_form.get('login', '')
    password = web_form.get('password', '')
    is_internal = True if web_form.get('is_internal') == 'on' else False

    if not login or not password:
        return AuthUserResponse(data=None, status=False, error_message='Wrong input. Repeat')

    if not is_internal:
        # make external API call
        response = requests.get(
            f'http://127.0.0.1:5002/api/auth/find-user',
            headers={'Authorization': create_basic_auth_token(login, password)}
        )

        resp_json = response.json()
        if resp_json['status'] == 200:
            return AuthUserResponse(data=resp_json['user'], status=True, error_message='')
    else:
        # find internal user
        sql = provider.get('user.sql', dict(login=login, password=password))
        user = select_dict(db_config, sql)
        if user:
            return AuthUserResponse(data=user[0], status=True, error_message='')

    return AuthUserResponse(data=None, status=False, error_message='User not found')
