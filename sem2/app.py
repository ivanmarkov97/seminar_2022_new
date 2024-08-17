from flask import Flask, render_template, request

from operations import select


app = Flask(__name__)

db_config = {
    'host': '127.0.0.1',
    'port': 3307,
    'user': 'root',
    'password': 'root',
    'database': 'supermarket'
}


@app.route('/')
@app.route('/<param>')
def index(param=None):
    if param is None:
        return "Hello world"
    else:
        return f"Hello {param}"


@app.route('/menu')
def render_menu():
    return render_template('menu.html')


@app.route('/exit')
def exit_is():
    return "Goodbye!"


@app.route('/product', methods=['GET', 'POST'])
def find_product():
    if request.method == 'GET':
        return render_template('product_form.html')
    else:
        input_product = request.form.get('product_name')
        if input_product:
            sql = f"""
                SELECT 
                    prod_id, 
                    prod_name,
                    prod_price
                FROM product 
                WHERE 1=1
                    AND prod_name LIKE '%{input_product}%'
            """
            prod_result, schema = select(db_config, sql)
            if prod_result:
                return render_template('db_result.html', schema=schema, result=prod_result)
            return 'Ничего не найдено'
        return "Try again"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
