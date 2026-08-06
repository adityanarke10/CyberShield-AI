from flask import Flask, render_template
from flask_login import LoginManager
from extensions import bcrypt

from config import Config
from models import db
from models.user import User

from routes.auth import auth
from routes.dashboard import dashboard
from routes.scanner import scanner
from routes.reports import reports
from routes.api import api
from models.scan_history import ScanHistory

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

bcrypt.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(scanner)
app.register_blueprint(reports)
app.register_blueprint(api)


@app.route("/")
def home():
    return render_template("index.html")


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)


