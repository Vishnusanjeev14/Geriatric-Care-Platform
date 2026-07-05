from flask import flash, redirect, render_template, request, session, url_for

from app.extensions import db
from app.models import Account
from app.permissions.decorators import login_required
from app.services.auth_service import current_account, login_account, logout_account, signup_account

from . import auth_bp


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        session.clear()
        return render_template("auth/login.html")
    if request.method == "POST":
        account = login_account(request.form["email"], request.form["password"])
        if not account:
            flash("Email or password is incorrect.", "error")
            return render_template("auth/login.html"), 401
        if account.account_type == "healthcare":
            return redirect(url_for("healthcare.dashboard"))
        if account.account_type == "caretaker":
            return redirect(url_for("caretaker_portal.dashboard"))
        return redirect(url_for("profiles.choose"))


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        try:
            signup_account(
                request.form["full_name"],
                request.form["email"],
                request.form["password"],
                request.form.get("account_type", "family"),
            )
        except ValueError as error:
            flash(str(error), "error")
            return render_template("auth/signup.html"), 400
        flash("Account created. Please sign in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/signup.html")


@auth_bp.post("/logout")
def logout():
    logout_account()
    flash("You have been signed out.", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/account", methods=["GET", "POST"])
@login_required
def account():
    account = current_account()
    if request.method == "POST":
        full_name = request.form["full_name"].strip()
        email = request.form["email"].strip().lower()
        phone = request.form.get("phone", "").strip() or None
        if not full_name:
            flash("Full name is required.", "error")
            return render_template("auth/account.html", account=account), 400
        if not email:
            flash("Email is required.", "error")
            return render_template("auth/account.html", account=account), 400
        existing = Account.query.filter(Account.email == email, Account.id != account.id).first()
        if existing:
            flash("Another account already uses that email.", "error")
            return render_template("auth/account.html", account=account), 400
        account.full_name = full_name
        account.email = email
        account.phone = phone
        db.session.commit()
        flash("Account profile updated.", "success")
        return redirect(url_for("auth.account"))
    return render_template("auth/account.html", account=account)


@auth_bp.post("/language")
def language():
    language_code = request.form.get("language", "en")
    session["language"] = language_code
    account = None
    try:
        from app.extensions import db
        from app.services.auth_service import current_account

        account = current_account()
        if account:
            account.preferred_language = language_code
            db.session.commit()
    except Exception:
        pass
    return redirect(request.referrer or url_for("main.index"))
