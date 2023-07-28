import json
from base64 import b64decode

from flask import Flask, request, make_response

from database.operations import select
from database.sql_provider import SQLProvider


app = Flask(__name__)
app.config['DB_CONFIG'] = json.load(open('configs/db.json'))

sql_provider = SQLProvider('sql/')


def validate_request(request):
    if 'Authorization' not in request.headers:
        return False
    if 'Basic ' not in request.headers['Authorization']:
        return False
    if len(request.headers['Authorization']) <= len('Basic ') + 3: # minimum content size
        return False
    return True

def get_user_credentials(request):
    # get raw token
    header = request.headers['Authorization']
    start_token_index = header.index(" ") + 1  # skip "Basic" part
    token = header[start_token_index:]

    # decode base64 token
    user_credentials = b64decode(token.encode('utf-8')).decode('utf-8')
    login, password = user_credentials.split(':')
    return {'login': login, 'password': password}


@app.route('/api/v1/user', methods=['GET'])
def find_user():
    if not validate_request(request):
        response = make_response("")
        response.headers['Content-Type'] = 'application/json'
        response.status_code = 400  # Bad request
        return response

    user_credentials = get_user_credentials(request)

    # search user in DB
    user_data = select(
        app.config['DB_CONFIG'],
        sql_provider.get(
            'get_user.sql',
            login=user_credentials['login'],
            password=user_credentials['password']
        )
    )
    # if no such user
    if not user_data:
        response = make_response("")
        response.headers['Content-Type'] = 'application/json'
        response.status_code = 404  # not found
        return response

    # send response with user data
    user_info = {
        'user_id': user_data[0]['user_id'],
        'user_group': user_data[0]['user_group']
    }
    json_data = json.dumps(user_info)
    response = make_response(json_data)
    response.headers['Content-Type'] = 'application/json'
    response.status_code = 200
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002)
