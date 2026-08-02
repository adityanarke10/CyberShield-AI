from flask import Blueprint, render_template

from forms.auth_forms import RegisterForm

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    return render_template(
        "register.html",
        form=form
    )


@auth.route("/login")
def login():

    return render_template("login.html")