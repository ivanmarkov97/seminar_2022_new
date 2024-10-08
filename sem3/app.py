from flask import Flask, render_template, json

from query.route import blueprint_query
from report.route import blueprint_report


app = Flask(__name__)

app.register_blueprint(blueprint_query, url_prefix='/query')
app.register_blueprint(blueprint_report, url_prefix='/report')

app.config['db_config'] = json.load(open('configs/dbconfig.json'))


@app.route('/', methods=['GET', 'POST'])
def query():
    return render_template('start_request.html')


@app.route('/exit')
def goodbye():
    return 'До свидания, заходите к нам еще!'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
