import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "cybershield_ai_2026_secret_key"
    )

    database_path = os.path.join(
        BASE_DIR,
        "database",
        "cybershield.db"
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + database_path
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False