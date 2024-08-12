from __future__ import annotations

from functools import wraps
from typing import Callable, Any

from flask import session, render_template, current_app, request, redirect, url_for


def login_required(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        if 'user_id' in session:
            return func(*args, **kwargs)
        return redirect(url_for('blueprint_auth.start_auth'))
    return wrapper


def group_validation(config: dict) -> bool:
    endpoint_app: str = request.endpoint.split('.')[0]
    if 'user_group' in session:
        user_group: dict = session['user_group']
        if user_group in config and endpoint_app in config[user_group]:
            return True
    return False


def group_required(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        config: dict = current_app.config['access_config']
        if group_validation(config):
            return func(*args, **kwargs)
        return render_template('exceptions/internal_only.html')
    return wrapper


def external_validation(config: dict) -> bool:
    endpoint_app: str = request.endpoint.split('.')[0]
    user_id: str | None = session.get('user_id', None)
    user_group: str | None = session.get('user_group', None)
    if user_id and user_group is None:
        if endpoint_app in config['external']:
            return True
    return False


def external_required(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        config: dict = current_app.config['access_config']
        if external_validation(config):
            return func(*args, **kwargs)
        return render_template('exceptions/external_only.html')
    return wrapper
