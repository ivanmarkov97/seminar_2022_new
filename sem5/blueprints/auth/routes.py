import os

from flask import (
	Blueprint, session, render_template, request, current_app, redirect)

from database.connection import DBConnection
from database.sql_provider import SQLProvider


auth_app = Blueprint('auth', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@auth_app.route('/login', methods=['GET', 'POST'])
def login_page():
	if request.method == 'GET':
		return render_template('login.html')
	else:
		token = None
		login = request.form['login']
		password = request.form['password']
		with DBConnection(current_app.config['DB_CONFIG']) as cursor:
			sql = provider.get('user.sql', login=login, password=password)
			cursor.execute(sql)
			user = cursor.fetchone()
			if user:
				schema = [column[0] for column in cursor.description]
				user = dict(zip(schema, user))
				group_name = user['group_name']
				session['group'] = group_name
				session.permanent = True
				return redirect('/')
		if token is None:
			return render_template('login.html', message='Invalid login or password')


@auth_app.route('/logout')
def logout():
	session.clear()
	return redirect('/')
