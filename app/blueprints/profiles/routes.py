from flask import abort, flash, redirect, render_template, request, url_for

from app.extensions import db
from app.models import (
    AccountProfilePermission,
    Appointment,
    CareRequest,
    EmergencyContact,
    MedicalCondition,
    MedicineSchedule,
    Notification,
    Profile,
    TimelineEvent,
)
from app.permissions.decorators import account_type_required
from app.services.auth_service import current_account
from app.services.profile_service import create_profile, select_profile, update_profile
from app.services.schedule_service import due_today

from . import profiles_bp


def _profile_or_404(profile_id):
    account = current_account()
    profile = select_profile(account.id, profile_id)
    if not profile:
        abort(404)
    return profile


@profiles_bp.route("/new", methods=["GET", "POST"])
@account_type_required("family")
def new_profile():
    if request.method == "POST":
        create_profile(current_account().id, request.form)
        flash("Profile created.", "success")
        return redirect(url_for("family.workspace"))
    return render_template("profiles/new.html")


@profiles_bp.get("/choose")
@account_type_required("family")
def choose():
    from app.services.profile_service import managed_profiles

    profiles = managed_profiles(current_account().id)
    return render_template("profiles/choose.html", profiles=profiles)


@profiles_bp.get("/<int:profile_id>/select")
@account_type_required("family")
def select(profile_id):
    if not select_profile(current_account().id, profile_id):
        abort(404)
    return redirect(url_for("profiles.dashboard", profile_id=profile_id))


@profiles_bp.get("/<int:profile_id>/dashboard")
@account_type_required("family")
def dashboard(profile_id):
    profile = _profile_or_404(profile_id)
    schedules = MedicineSchedule.query.filter_by(profile_id=profile.id, status="active").all()
    due_records = due_today(profile.id)
    appointments = Appointment.query.filter_by(profile_id=profile.id).order_by(Appointment.appointment_date).limit(3).all()
    care_request = CareRequest.query.filter_by(profile_id=profile.id).order_by(CareRequest.created_at.desc()).first()
    contacts = EmergencyContact.query.filter_by(profile_id=profile.id).order_by(EmergencyContact.priority).all()
    conditions = MedicalCondition.query.filter_by(profile_id=profile.id).all()
    timeline = TimelineEvent.query.filter_by(profile_id=profile.id).order_by(TimelineEvent.created_at.desc()).limit(6).all()
    return render_template(
        "profiles/dashboard.html",
        profile=profile,
        schedules=schedules,
        due_records=due_records,
        appointments=appointments,
        care_request=care_request,
        contacts=contacts,
        conditions=conditions,
        timeline=timeline,
    )


@profiles_bp.route("/<int:profile_id>/edit", methods=["GET", "POST"])
@account_type_required("family")
def edit(profile_id):
    profile = _profile_or_404(profile_id)
    if request.method == "POST":
        update_profile(profile, request.form, current_account().id)
        flash("Profile updated.", "success")
        return redirect(url_for("profiles.dashboard", profile_id=profile.id))
    return render_template("profiles/edit.html", profile=profile)


@profiles_bp.get("/<int:profile_id>/emergency")
@account_type_required("family")
def emergency(profile_id):
    profile = _profile_or_404(profile_id)
    contacts = EmergencyContact.query.filter_by(profile_id=profile.id).order_by(EmergencyContact.priority).all()
    conditions = MedicalCondition.query.filter_by(profile_id=profile.id).all()
    schedules = MedicineSchedule.query.filter_by(profile_id=profile.id, status="active").all()
    return render_template("profiles/emergency.html", profile=profile, contacts=contacts, conditions=conditions, schedules=schedules)


@profiles_bp.get("/<int:profile_id>/timeline")
@account_type_required("family")
def timeline(profile_id):
    profile = _profile_or_404(profile_id)
    events = TimelineEvent.query.filter_by(profile_id=profile.id).order_by(TimelineEvent.created_at.desc()).all()
    return render_template("profiles/timeline.html", profile=profile, events=events)


@profiles_bp.route("/<int:profile_id>/sharing", methods=["GET", "POST"])
@account_type_required("family")
def sharing(profile_id):
    profile = _profile_or_404(profile_id)
    if request.method == "POST":
        db.session.add(
            Notification(
                account_id=current_account().id,
                profile_id=profile.id,
                category="family_access",
                priority="normal",
                title="Invitation prepared",
                message=f"Prototype invite prepared for {request.form['email']} as {request.form['role']}.",
            )
        )
        db.session.commit()
        flash("Prototype invitation recorded.", "success")
    permissions = AccountProfilePermission.query.filter_by(profile_id=profile.id).all()
    return render_template("profiles/sharing.html", profile=profile, permissions=permissions)
