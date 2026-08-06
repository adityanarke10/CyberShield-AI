from flask import Blueprint, render_template
from flask_login import login_required

from models.scan_history import ScanHistory

history = Blueprint("history", __name__)


@history.route("/history")
@login_required
def history_page():

    scans = (
        ScanHistory.query
        .order_by(ScanHistory.scan_date.desc())
        .all()
    )

    return render_template(
        "history.html",
        scans=scans
    )