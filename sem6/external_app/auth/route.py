import os

from flask import Blueprint, request, jsonify, current_app

from database.sql_provider import SQLProvider
from .user import find_user


blueprint_auth = Blueprint('blueprint_auth', __name__)
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_auth.route('/find-user', methods=['GET'])
def find_user_handler():
    return jsonify(find_user(request, provider, current_app.config['db_config']))
