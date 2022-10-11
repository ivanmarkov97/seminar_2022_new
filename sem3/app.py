from flask import Flask, url_for, request, render_template, redirect, json
from blueprint_query.route import blueprint_query
from blueprint_report.route import blueprint_report

app = Flask(__name__)

app.register_blueprint(blueprint_query, url_prefix='/zaproses')
app.register_blueprint(blueprint_report, url_prefix='/reports')

with open('data_files/dbconfig.json', 'r') as f:
    db_config = json.load(f)
app.config['dbconfig'] = db_config


@app.route('/', methods=['GET', 'POST'])
def query():
    return render_template('start_request.html')

@app.route('/exit')
def goodbye():
    return 'До свиданья, заходите к нам еще!'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
