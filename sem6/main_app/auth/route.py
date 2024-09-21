import os

from flask import Blueprint, request, render_template, session, redirect, url_for, current_app

from database.sql_provider import SQLProvider
from .auth_user import find_user_with_form


blueprint_auth = Blueprint('bp_auth', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


def save_in_session_and_redirect(user_dict):
    session['user_id'] = user_dict['user_id']
    session['user_group'] = user_dict['user_group']
    session.permanent = True
    return redirect(url_for('menu_choice'))


@blueprint_auth.route('/', methods=['GET'])
def auth_input_handler():
    return render_template('input_login.html', message='')


@blueprint_auth.route('/', methods=['POST'])
def auth_process_handler():
    response = find_user_with_form(request.form, current_app.config['db_config'], provider)
    if response.status:
        return save_in_session_and_redirect(response.data)
    return render_template('input_login.html', message=response.error_message)
