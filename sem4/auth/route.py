import os

from flask import Blueprint, request, render_template, current_app, session, redirect, url_for

from database.sql_provider import SQLProvider
from .auth_user import find_user_with_form


blueprint_auth = Blueprint('bp_auth', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


def set_user_session(session, web_form, db_config, provider):
    user_response = find_user_with_form(web_form, db_config, provider)
    if user_response.status:
        session['user_id'] = user_response.data['user_id']
        session['user_group'] = user_response.data['user_group']
        session.permanent = True
        return redirect(url_for('menu_choice'))
    return render_template('input_login.html', message=user_response.error_message)


@blueprint_auth.route('/', methods=['GET'])
def auth_input_handler():
    return render_template('input_login.html', message='')


@blueprint_auth.route('/', methods=['POST'])
def auth_process_handler():
    return set_user_session(session, request.form, current_app.config['db_config'], provider)
