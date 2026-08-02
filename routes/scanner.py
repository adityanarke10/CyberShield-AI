from flask import Blueprint, render_template

scanner = Blueprint("scanner", __name__)

@scanner.route("/scan")
def scan():
    return render_template("scan.html")