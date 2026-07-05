from flask import render_template

from app.models import Notification, TimelineEvent
from app.permissions.decorators import account_type_required
from app.services.auth_service import current_account
from app.services.profile_service import managed_profiles

from . import family_bp


@family_bp.get("/workspace")
@account_type_required("family")
def workspace():
    account = current_account()
    profiles = managed_profiles(account.id)
    notifications = Notification.query.filter_by(account_id=account.id).order_by(Notification.created_at.desc()).limit(6).all()
    profile_ids = [profile.id for profile in profiles]
    events = TimelineEvent.query.filter(TimelineEvent.profile_id.in_(profile_ids)).order_by(TimelineEvent.created_at.desc()).limit(8).all() if profile_ids else []
    return render_template("family/workspace.html", profiles=profiles, notifications=notifications, events=events)


@family_bp.get("/view")
@account_type_required("family")
def family_view():
    account = current_account()
    profiles = managed_profiles(account.id)
    return render_template("family/family_view.html", profiles=profiles)
