import json

from flask import Flask, render_template
from query.routes import blueprint_query


app = Flask(__name__)

app.register_blueprint(blueprint_query, url_prefix='/requests')
app.config['db_config'] = json.load(open('configs/db.json'))


@app.route('/', methods=['GET', 'POST'])
def query():
    return render_template('start_request.html')


@app.route('/exit')
def goodbye():
    return 'Goodbye!'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
