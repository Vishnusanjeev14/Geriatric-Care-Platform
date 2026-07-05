from datetime import datetime

from flask import session

from app.extensions import db
from app.models import (
    AccountProfilePermission,
    EmergencyContact,
    MedicalCondition,
    Profile,
    ProfileAddress,
    TimelineEvent,
)


def managed_profiles(account_id):
    return (
        Profile.query.join(AccountProfilePermission)
        .filter(AccountProfilePermission.account_id == account_id)
        .filter(Profile.status == "active")
        .order_by(Profile.display_name)
        .all()
    )


def active_profile(account_id):
    profile_id = session.get("active_profile_id")
    profiles = managed_profiles(account_id)
    if not profiles:
        return None
    if profile_id and any(profile.id == profile_id for profile in profiles):
        return db.session.get(Profile, profile_id)
    return None


def select_profile(account_id, profile_id):
    profile = (
        Profile.query.join(AccountProfilePermission)
        .filter(AccountProfilePermission.account_id == account_id)
        .filter(Profile.id == profile_id)
        .first()
    )
    if profile:
        session["active_profile_id"] = profile.id
    return profile


def create_profile(account_id, form):
    profile = Profile(
        display_name=form["display_name"].strip(),
        relationship_label=form.get("relationship_label", "Family").strip() or "Family",
        date_of_birth=datetime.strptime(form["date_of_birth"], "%Y-%m-%d").date(),
        gender=form.get("gender"),
        photo_initials=_initials(form["display_name"]),
        blood_group=form.get("blood_group"),
        health_status=form.get("health_status", "stable"),
        primary_hospital=form.get("primary_hospital"),
        primary_care_note=form.get("primary_care_note"),
    )
    db.session.add(profile)
    db.session.flush()
    db.session.add(AccountProfilePermission(account_id=account_id, profile_id=profile.id, role="owner"))
    if form.get("line1"):
        db.session.add(
            ProfileAddress(
                profile_id=profile.id,
                label="Home",
                line1=form["line1"],
                city=form.get("city", ""),
                state=form.get("state", ""),
                postal_code=form.get("postal_code", ""),
                is_default=True,
            )
        )
    if form.get("emergency_name") and form.get("emergency_phone"):
        db.session.add(
            EmergencyContact(
                profile_id=profile.id,
                name=form["emergency_name"],
                relationship=form.get("emergency_relationship", "Family"),
                phone=form["emergency_phone"],
            )
        )
    if form.get("condition_name"):
        db.session.add(MedicalCondition(profile_id=profile.id, name=form["condition_name"], severity="monitoring"))
    add_timeline(profile.id, account_id, "Profile created", "A new care profile was added.", "profiles")
    db.session.commit()
    session["active_profile_id"] = profile.id
    return profile


def update_profile(profile, form, actor_id):
    profile.display_name = form["display_name"].strip()
    profile.relationship_label = form.get("relationship_label", profile.relationship_label)
    profile.blood_group = form.get("blood_group")
    profile.health_status = form.get("health_status", profile.health_status)
    profile.primary_hospital = form.get("primary_hospital")
    profile.primary_care_note = form.get("primary_care_note")
    add_timeline(profile.id, actor_id, "Profile updated", "Basic profile information was updated.", "profiles")
    db.session.commit()


def add_timeline(profile_id, account_id, title, description, source_module, priority="normal"):
    db.session.add(
        TimelineEvent(
            profile_id=profile_id,
            actor_account_id=account_id,
            event_type=title.lower().replace(" ", "_"),
            title=title,
            description=description,
            source_module=source_module,
            priority=priority,
        )
    )


def _initials(name):
    parts = [part[0] for part in name.strip().split() if part]
    return "".join(parts[:2]).upper() or "CC"
