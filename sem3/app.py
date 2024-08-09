from flask import Flask, render_template, json

from blueprint_query.route import blueprint_query
from blueprint_report.route import blueprint_report


app: Flask = Flask(__name__)

app.register_blueprint(blueprint_query, url_prefix='/requests')
app.register_blueprint(blueprint_report, url_prefix='/reports')

app.config['dbconfig'] = json.load(open('data_files/dbconfig.json'))


@app.route('/', methods=['GET', 'POST'])
def query() -> str:
    return render_template('start_request.html')


@app.route('/exit')
def goodbye() -> str:
    return 'До свидания, заходите к нам еще!'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
