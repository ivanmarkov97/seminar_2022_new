from functools import wraps

from flask import request, render_template, session, current_app


def login_validation(session: session) -> bool:
	group = session.get('group', None)
	if group is not None and group != '':
		return True
	return False


def group_validation(config: dict, request: request) -> bool:
	endpoint_app = '' if len(request.endpoint.split('.')) == 1 else request.endpoint.split('.')[0]
	if endpoint_app in config['unauthorized']:
		return True
	elif 'group' in session:
		group = session['group']
		if group in config and endpoint_app in config[group]:
			return True
	return False


class AccessManager:

	@staticmethod
	def login_required(f):
		@wraps(f)
		def wrapper(*args, **kwargs):
			if login_validation(session):
				return f(*args, **kwargs)
			return render_template('permission.html')
		return wrapper

	@staticmethod
	def group_required(f):
		@wraps(f)
		def wrapper(*args, **kwargs):
			config = current_app.config['ACCESS_CONFIG']
			if group_validation(config, request):
				return f(*args, **kwargs)
			return render_template('permission.html')
		return wrapper
