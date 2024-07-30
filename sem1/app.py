from typing import List, Dict, Union

from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def hello() -> str:
    return "Hello world"


@app.route('/static')
def static_index() -> str:
    return render_template('static_index.html')


@app.route('/dynamic')
def dynamic_index() -> str:
    products: List[Dict[str, Union[str, int]]] = [
        {'name': 'телятина', 'measure': 'килограмм', 'price': 800},
        {'name': 'говядина', 'measure': 'килограмм', 'price': 710},
        {'name': 'свинина', 'measure': 'килограмм', 'price': 670},
    ]
    product_title = 'Вот все наши мясные продукты'
    return render_template('dynamic_index.html', product_title=product_title, products=products)


@app.route('/test')
def test_index() -> str:
    return "Changes are done"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
