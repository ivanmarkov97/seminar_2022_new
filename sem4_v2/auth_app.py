from __future__ import annotations

import json

from flask import Flask, current_app, request

from database.sql_provider import SQLProvider
from database.db_work import select_dict


app: Flask = Flask(__name__)
app.config['db_config'] = json.load(open('configs/db.json'))

provider: SQLProvider = SQLProvider(file_path='auth/sql')


@app.route('/find-user/internal', methods=['POST'])
def find_internal_user() -> dict[str, int | str]:
    return find_user(request.json['login'], request.json['password'], user_type='internal')


@app.route('/find-user/external', methods=['POST'])
def find_external_user() -> dict[str, int | str]:
    return find_user(request.json['login'], request.json['password'], user_type='external')


def find_user(login: str, password: str, user_type: str) -> dict[str, int | str]:
    query_mapping: dict[str, str] = {
        'internal': 'internal_user.sql',
        'external': 'external_user.sql'
    }

    if user_type not in ['internal', 'external']:
        raise ValueError('Invalid user type')

    sql: str = provider.get(query_mapping[user_type], dict(login=login, password=password))
    user_or_none: list[dict] | None = select_dict(current_app.config['db_config'], sql)

    if not user_or_none or not user_or_none[0]:
        return {
            'status': 404,
            'message': 'not found'
        }
    return {
        'status': 200,
        'message': 'OK',
        'user': user_or_none[0]
    }


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002)
