from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.scan_history import ScanHistory
from models import db
from sqlalchemy import func

profile = Blueprint("profile", __name__)


@profile.route("/profile")
@login_required
def profile_page():

    total_scans = ScanHistory.query.count()

    average_score = db.session.query(
        func.avg(ScanHistory.security_score)
    ).scalar() or 0

    average_score = round(average_score)

    low_risk = ScanHistory.query.filter_by(
        risk_level="Low"
    ).count()

    high_risk = ScanHistory.query.filter_by(
        risk_level="High"
    ).count()

    recent_scans = (
        ScanHistory.query
        .order_by(ScanHistory.scan_date.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "profile.html",
        total_scans=total_scans,
        average_score=average_score,
        low_risk=low_risk,
        high_risk=high_risk,
        recent_scans=recent_scans
    )