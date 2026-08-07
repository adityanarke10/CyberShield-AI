from flask_login import current_user
from flask import Blueprint, render_template, request
from models.scan_history import ScanHistory
from models import db

from scanner.website_info import scan_website
from scanner.header_scan import scan_headers
from scanner.ssl_scan import scan_ssl
from scanner.technology_scan import detect_technology
from scanner.cookie_scan import scan_cookies

from security.score import calculate_security_score

scanner = Blueprint("scanner", __name__)


@scanner.route("/scan", methods=["GET", "POST"])
def scan():

    result = None
    headers = None
    ssl_info = None
    technologies = None
    cookies = None
    security_score = None
    scan = None

    if request.method == "POST":

        url = request.form.get("url")

        try:

            # Website Information
            result = scan_website(url)

            # Security Headers
            headers = scan_headers(url)

            # SSL Certificate
            ssl_info = scan_ssl(url)

            # Technology Detection
            technologies = detect_technology(url)

            # Cookie Analysis
            cookies = scan_cookies(url)

            # Security Score
            security_score = calculate_security_score(
                result,
                headers,
                ssl_info,
                cookies
            )

            history = ScanHistory(
                website=result["url"],
                security_score=security_score["score"],
                risk_level=security_score["risk"],
                user_id=current_user.id
            )

            db.session.add(history)
            db.session.commit()

            scan = history

        except Exception as e:

            result = {
                "error": str(e)
            }

    return render_template(
        "scan.html",
        result=result,
        headers=headers,
        ssl_info=ssl_info,
        technologies=technologies,
        cookies=cookies,
        security_score=security_score,
        scan=scan
    )