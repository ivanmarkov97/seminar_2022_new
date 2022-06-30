from flask import Flask, url_for, request, render_template, redirect, session
from blueprint_auth.blueprint_auth import blueprint_auth
from blueprint_report.blueprint_report import blueprint_report

app = Flask(__name__)


app.register_blueprint(blueprint_auth)
app.register_blueprint(blueprint_report)
app.secret_key = 'SuperKey'
app.config['dbconfig'] = {'host': '127.0.0.1', 'user': 'root', 'password': 'root', 'database': 'supermarket'}
app.config['access_config'] = {
  "group1": [
      "blueprint_report",
      "blueprint_basket",
  ],
  "admin": [
      "blueprint_basket",
      "blueprint_report",
      "blueprint_report.start_report"
  ]

}

@app.route('/')
def start_point():
    return redirect(url_for('blueprint_auth.start_auth'))

@app.route('/menu_choice')
def menu_choice():

    if session['user_type'] == 2:
        return render_template('external_user_menu.html')
    elif session['user_type'] == 1:
        return render_template('internal_user_menu.html')



@app.route('/exit')
def exit_func():
    session.pop('user_type')
    session.pop('user_identity')
    return "До свиданья"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
