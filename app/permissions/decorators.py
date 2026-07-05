from functools import wraps

from flask import flash, redirect, request, session, url_for

from app.services.auth_service import current_account
from app.services.profile_service import active_profile


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_account():
            flash("Please sign in to continue.", "warning")
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


def account_type_required(*account_types):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            account = current_account()
            if not account:
                flash("Please sign in to continue.", "warning")
                return redirect(url_for("auth.login", next=request.path))
            if account.account_type not in account_types:
                flash("That workspace is not available for this account.", "error")
                return redirect(_home_for(account.account_type))
            if (
                account.account_type == "family"
                and "family" in account_types
                and not active_profile(account.id)
                and request.endpoint not in {"profiles.choose", "profiles.new_profile", "profiles.select", "auth.logout", "auth.language"}
            ):
                return redirect(url_for("profiles.choose"))
            return view(*args, **kwargs)

        return wrapped

    return decorator


def _home_for(account_type):
    if account_type == "healthcare":
        return url_for("healthcare.dashboard")
    if account_type == "caretaker":
        return url_for("caretaker_portal.dashboard")
    return url_for("profiles.choose")
