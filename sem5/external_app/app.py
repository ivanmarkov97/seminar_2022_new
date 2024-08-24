import json
from pathlib import Path

from flask import Flask

from blueprints.auth.route import blueprint_auth
from blueprints.market.route import blueprint_market


app = Flask(__name__)

project_path = Path(__file__).resolve().parent
app.config['db_config'] = json.load(open(project_path / 'configs/db.json'))

app.register_blueprint(blueprint_auth, url_prefix='/api/auth')
app.register_blueprint(blueprint_market, url_prefix='/api/market')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002)
