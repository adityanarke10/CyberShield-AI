from flask import Blueprint, render_template, request

from scanner.website_info import scan_website
from scanner.header_scan import scan_headers
from scanner.ssl_scan import scan_ssl

scanner = Blueprint("scanner", __name__)


@scanner.route("/scan", methods=["GET", "POST"])
def scan():

    result = None
    headers = None
    ssl_info = None

    if request.method == "POST":

        url = request.form.get("url")

        try:

            result = scan_website(url)

            headers = scan_headers(url)

            ssl_info = scan_ssl(url)

        except Exception as e:

            result = {
                "error": str(e)
            }

    return render_template(
        "scan.html",
        result=result,
        headers=headers,
        ssl_info=ssl_info
    )