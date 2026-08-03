from flask import Blueprint, render_template

report = Blueprint("report", __name__)


@report.route("/report")
def index():
    return render_template("report.html")