from flask import Blueprint, render_template, request

from scanner.website_info import scan_website
from scanner.header_scan import scan_headers

scanner = Blueprint("scanner", __name__)


@scanner.route("/scan", methods=["GET", "POST"])
def scan():

    result = None
    headers = None

    if request.method == "POST":

        url = request.form.get("url")

        try:

            # Website Information
            result = scan_website(url)

            # Security Headers
            headers = scan_headers(url)

        except Exception as e:

            result = {
                "error": str(e)
            }

    return render_template(
        "scan.html",
        result=result,
        headers=headers
    )