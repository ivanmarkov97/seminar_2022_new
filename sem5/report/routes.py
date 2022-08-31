from flask import Blueprint, render_template

blueprint_report = Blueprint('blueprint_report', __name__, template_folder='templates')


@blueprint_report.route('/')
def start_report():
    return render_template('report_result.html')
