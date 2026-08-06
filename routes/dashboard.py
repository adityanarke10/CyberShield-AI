from models import db
from flask import Blueprint, render_template
from flask_login import login_required
from flask import redirect, url_for
from models.scan_history import ScanHistory

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
@login_required
def index():
    recent_scans = (
        ScanHistory.query
        .order_by(ScanHistory.scan_date.desc())
        .limit(4)
        .all()
    )

    latest_activity = (
        ScanHistory.query
        .order_by(ScanHistory.scan_date.desc())
        .limit(4)
        .all()
    )

    return render_template(
        "dashboard.html",
        recent_scans=recent_scans,
        latest_activity=latest_activity
    )
@dashboard.route("/history")
@login_required
def history():

    scans = (
        ScanHistory.query
        .order_by(ScanHistory.scan_date.desc())
        .all()
    )

    return render_template(
        "history.html",
        scans=scans
    )
@dashboard.route("/delete-scan/<int:id>")
@login_required
def delete_scan(id):

    scan = ScanHistory.query.get_or_404(id)

    db.session.delete(scan)
    db.session.commit()

    return redirect(url_for("dashboard.history"))