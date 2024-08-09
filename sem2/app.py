from flask import Flask, render_template, request

from db_work import select


app: Flask = Flask(__name__)

db_config: dict = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'root',
    'database': 'supermarket'
}


@app.route('/')
@app.route('/<param>')
def index(param: str | None = None) -> str:
    if param is None:
        return "Hello world"
    else:
        return f"Hello {param}"


@app.route('/menu')
def render_menu() -> str:
    return render_template('menu.html')


@app.route('/page1')
def page1() -> str:
    return "Page 1"


@app.route('/page2')
def page2() -> str:
    return "Page 2"


@app.route('/exit')
def exit_is() -> str:
    return "Goodbye!"


@app.route('/product', methods=['GET', 'POST'])
def find_product() -> str:
    if request.method == 'GET':
        return render_template('product_form.html')
    else:
        input_product: str | None = request.form.get('product_name')
        if input_product:
            sql: str = f"""
                SELECT 
                    prod_id, 
                    prod_name,
                    prod_price
                FROM product 
                WHERE 1=1
                    AND prod_name ='{input_product}'
            """
            prod_result, schema = select(db_config, sql)
            return render_template('db_result.html', schema=schema, result=prod_result)
        return "Try again"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
