import json

from flask import Flask, render_template

app = Flask(__name__)

app.config['DB_CONFIG'] = json.load(open('configs/db.json'))
app.config['ACCESS_CONFIG'] = json.load(open('configs/access.json'))
app.config['SECRET_KEY'] = 'super secret key'


from blueprints.auth.routes import auth_app
from blueprints.basket.routes import basket_app

app.register_blueprint(auth_app, url_prefix='/')
app.register_blueprint(basket_app, url_prefix='/order')


@app.route('/')
def index():
	return render_template('index.html')


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5001)
