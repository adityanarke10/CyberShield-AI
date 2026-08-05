from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import logout_user, login_required, login_user

from forms.auth_forms import RegisterForm, LoginForm
from models.user import User
from models import db
from extensions import bcrypt

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        existing_user = User.query.filter_by(email=form.email.data).first()

        if existing_user:
            flash("Email already registered.", "danger")
            return redirect(url_for("auth.register"))

        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")

        new_user = User(
            full_name=form.full_name.data,
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please login.", "success")

        return redirect(url_for("auth.login"))

    return render_template(
        "register.html",
        form=form
    )


@auth.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(
                user.password,
                form.password.data
        ):

            login_user(
                user,
                remember=form.remember.data
            )

            flash("Welcome back!", "success")

            return redirect(url_for("dashboard.index"))

        flash("Invalid email or password.", "danger")

    return render_template(
        "login.html",
        form=form
    )


@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out successfully.", "info")

    return redirect(url_for("auth.login"))