from flask_login import UserMixin
from datetime import datetime, timedelta
from models import db


def ist_now():
    return datetime.utcnow() + timedelta(hours=5, minutes=30)


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=ist_now
    )

    def __repr__(self):
        return f"<User {self.email}>"