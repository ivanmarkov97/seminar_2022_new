import json

from flask import Flask

from blueprints.auth.route import blueprint_auth
from utils import get_config_dir


app = Flask(__name__)

app.config['db_config'] = json.load(open(get_config_dir() / 'db.json'))
app.register_blueprint(blueprint_auth, url_prefix='/api/auth')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002)
