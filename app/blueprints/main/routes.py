from flask import jsonify, redirect, url_for

from app.services.auth_service import current_account
from app.services.profile_service import active_profile

from . import main_bp


@main_bp.get("/")
def index():
    account = current_account()
    if account and account.account_type == "family":
        profile = active_profile(account.id)
        if profile:
            return redirect(url_for("profiles.dashboard", profile_id=profile.id))
        return redirect(url_for("profiles.choose"))
    if account and account.account_type == "healthcare":
        return redirect(url_for("healthcare.dashboard"))
    if account and account.account_type == "caretaker":
        return redirect(url_for("caretaker_portal.dashboard"))
    return redirect(url_for("auth.login"))


@main_bp.get("/health")
def health_check():
    return jsonify({"status": "ok", "service": "CareConnect"})
