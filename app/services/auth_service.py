from datetime import datetime

from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.models import Account


def current_account():
    account_id = session.get("account_id")
    if not account_id:
        return None
    return db.session.get(Account, account_id)


def login_account(email, password):
    account = Account.query.filter_by(email=email.strip().lower()).first()
    if not account or not check_password_hash(account.password_hash, password):
        return None
    if account.status != "active":
        return None
    account.last_login_at = datetime.utcnow()
    db.session.commit()
    session.clear()
    session["account_id"] = account.id
    session["account_type"] = account.account_type
    return account


def signup_account(full_name, email, password, account_type):
    normalized_email = email.strip().lower()
    if Account.query.filter_by(email=normalized_email).first():
        raise ValueError("An account already exists for that email.")
    account = Account(
        full_name=full_name.strip(),
        email=normalized_email,
        password_hash=generate_password_hash(password),
        account_type=account_type,
    )
    db.session.add(account)
    db.session.commit()
    return account


def logout_account():
    session.clear()
