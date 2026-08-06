from datetime import datetime
from models import db


class ScanHistory(db.Model):

    __tablename__ = "scan_history"

    id = db.Column(db.Integer, primary_key=True)

    website = db.Column(db.String(255), nullable=False)

    security_score = db.Column(db.Integer, nullable=False)

    risk_level = db.Column(db.String(50), nullable=False)

    scan_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )