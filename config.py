import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DB_FOLDER = os.path.join(BASE_DIR, "database")

os.makedirs(DB_FOLDER, exist_ok=True)

DB_PATH = os.path.join(DB_FOLDER, "cybershield.db")

SQLALCHEMY_DATABASE_URI = "sqlite:///" + DB_PATH

    SQLALCHEMY_TRACK_MODIFICATIONS = False