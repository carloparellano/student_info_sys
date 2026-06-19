from flask import render_template, redirect, flash, session, url_for
from .forms import LoginForm, RegisterForm
from .controller import create_user, verify_user
from . import user_bp


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect("/")
    form = LoginForm()
    if form.validate_on_submit():
        if verify_user(form.email.data, form.password.data):
            session["user"] = form.email.data
            flash("Logged in successfully!", "success")
            return redirect("/")
        else:
            flash("Invalid email or password.", "danger")
    return render_template("login.html", form=form)


@user_bp.route("/register", methods=["GET", "POST"])
def register():
    if "user" in session:
        return redirect("/")
    form = RegisterForm()
    if form.validate_on_submit():
        if create_user(form.email.data, form.password.data):
            flash("Account created! You can now log in.", "success")
            return redirect(url_for("users.login"))
        else:
            flash("Email already registered.", "danger")
    return render_template("register.html", form=form)


@user_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("users.login"))
