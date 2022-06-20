from flask import Flask, render_template, request
from db_work import work_with_db


app = Flask(__name__)

dbconfig = {'host': '127.0.0.1', 'user': 'root', 'password': 'root', 'database': 'supermarket'}


@app.route('/')
@app.route('/<param>')
def index(param=None):
    if param is None:
        return "Hello world"
    else:
        return f"Hello {param}"


@app.route('/reference')
def reference_redirect():
    return render_template('reference_redirect.html')


@app.route('/page1')
def page1():
    return "Я - страница 1"


@app.route('/page2')
def page2():
    return "Я - страница 2"


@app.route('/exit')
def exit_is():
    return "До свиданья, заходите к нам еще!"

@app.route('/find_product', methods=['GET','POST'])
def find_product():
    if request.method == 'GET':
        return render_template('product_form.html')
    else:
        input_product = request.form.get('product_name')
        if input_product:
            _sql = f""" select p_id, prod_name,prod_measure,prod_price
                    from product where prod_name ='{input_product}'"""
            prod_result, schema = work_with_db(dbconfig, _sql)
            for i in range(len(schema)):
                print(i)
            return render_template('db_result.html', schema=schema)
        else:
            return "Повторите ввод"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)

