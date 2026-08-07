from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func

from models import db
from models.scan_history import ScanHistory

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
@login_required
def index():

    # Recent scans (only current user)
    recent_scans = (
        ScanHistory.query
        .filter_by(user_id=current_user.id)
        .order_by(ScanHistory.scan_date.desc())
        .limit(4)
        .all()
    )

    # Latest activity (only current user)
    latest_activity = (
        ScanHistory.query
        .filter_by(user_id=current_user.id)
        .order_by(ScanHistory.scan_date.desc())
        .limit(4)
        .all()
    )

    # Dashboard Statistics
    total_scans = (
        ScanHistory.query
        .filter_by(user_id=current_user.id)
        .count()
    )

    high_risk = (
        ScanHistory.query
        .filter_by(
            user_id=current_user.id,
            risk_level="High"
        )
        .count()
    )

    protected = (
        ScanHistory.query
        .filter(
            ScanHistory.user_id == current_user.id,
            ScanHistory.security_score >= 80
        )
        .count()
    )

    reports_generated = total_scans

    avg_score = (
        db.session.query(func.avg(ScanHistory.security_score))
        .filter(ScanHistory.user_id == current_user.id)
        .scalar()
    )

    avg_score = round(avg_score or 0)

    return render_template(
        "dashboard.html",
        recent_scans=recent_scans,
        latest_activity=latest_activity,
        total_scans=total_scans,
        high_risk=high_risk,
        protected=protected,
        reports_generated=reports_generated,
        avg_score=avg_score
    )


@dashboard.route("/history")
@login_required
def history():

    scans = (
        ScanHistory.query
        .filter_by(user_id=current_user.id)
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

    scan = (
        ScanHistory.query
        .filter_by(
            id=id,
            user_id=current_user.id
        )
        .first_or_404()
    )

    db.session.delete(scan)
    db.session.commit()

    return redirect(url_for("dashboard.history"))