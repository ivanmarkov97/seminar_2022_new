from flask import Flask, url_for, request, render_template, redirect, json
from blueprint_query.blueprint_query import blueprint_query

app = Flask(__name__)


app.register_blueprint(blueprint_query, url_prefix='/zaproses')

app.config['dbconfig'] = {'host': '127.0.0.1', 'user': 'root', 'password': 'root', 'database': 'supermarket'}


@app.route('/', methods=['GET', 'POST'])
def query():
    return render_template('start_request.html')

@app.route('/exit')
def goodbye():
    return 'До свиданья, заходите к нам еще!'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
