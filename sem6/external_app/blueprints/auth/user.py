from base64 import b64decode

from database.operations import select_dict


def valid_authorization_request(api_request):
    auth_header = api_request.headers.get('Authorization', '')
    if not auth_header:
        return False
    if not auth_header.startswith('Basic '):
        return False
    if len(auth_header) <= len('Basic '):
        return False
    return True


def decode_basic_authorization(api_request):
    auth_header = api_request.headers.get('Authorization')
    token = auth_header.split()[-1]
    login_and_password = b64decode(token.encode('ascii')).decode('ascii').split(':')
    if len(login_and_password) != 2:
        raise ValueError('Invalid login and password format')
    login, password = login_and_password
    return login, password


def find_user(request, provider, db_config):
    if not valid_authorization_request(request):
        return {'status': 400, 'message': 'Bad request'}
    try:
        login, password = decode_basic_authorization(request)
    except Exception as e:
        return {'status': 400, 'message': f'Bad request. {str(e)}'}
    else:
        sql = provider.get('user.sql', dict(login=login, password=password))
        user = select_dict(db_config, sql)
        if not user:
            return {'status': 404, 'message': 'user not found'}
        return {'status': 200, 'message': 'OK', 'user': user[0]}
