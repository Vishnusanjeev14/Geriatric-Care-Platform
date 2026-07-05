from datetime import date

from flask import flash, redirect, render_template, request, url_for

from app.extensions import db
from app.models import CareRequest, Caretaker
from app.permissions.decorators import account_type_required
from app.services.auth_service import current_account

from . import caretaker_portal_bp


@caretaker_portal_bp.get("/login")
def login():
    return redirect(url_for("auth.login"))


@caretaker_portal_bp.get("/dashboard")
@account_type_required("caretaker")
def dashboard():
    caretaker = Caretaker.query.filter_by(account_id=current_account().id).first()
    available = CareRequest.query.filter_by(status="requested").order_by(CareRequest.created_at.desc()).all()
    assignments = (
        CareRequest.query.filter(CareRequest.caretaker_id == caretaker.id)
        .filter(CareRequest.status.in_(["accepted", "in_progress"]))
        .filter(CareRequest.start_date == date.today())
        .order_by(CareRequest.visit_time)
        .all()
        if caretaker
        else []
    )
    upcoming = (
        CareRequest.query.filter(CareRequest.caretaker_id == caretaker.id)
        .filter(CareRequest.status.in_(["accepted", "in_progress", "completed"]))
        .order_by(CareRequest.start_date, CareRequest.visit_time)
        .limit(8)
        .all()
        if caretaker
        else []
    )
    return render_template("caretaker/dashboard.html", caretaker=caretaker, available=available, assignments=assignments, upcoming=upcoming)


@caretaker_portal_bp.post("/requests/<int:request_id>/accept")
@account_type_required("caretaker")
def accept(request_id):
    caretaker = Caretaker.query.filter_by(account_id=current_account().id).first()
    care_request = db.session.get(CareRequest, request_id)
    care_request.caretaker_id = caretaker.id
    care_request.status = "accepted"
    db.session.commit()
    flash("Request accepted.", "success")
    return redirect(url_for("caretaker_portal.dashboard"))


@caretaker_portal_bp.post("/requests/<int:request_id>/decline")
@account_type_required("caretaker")
def decline(request_id):
    care_request = db.session.get(CareRequest, request_id)
    care_request.status = "cancelled"
    db.session.commit()
    flash("Request declined.", "success")
    return redirect(url_for("caretaker_portal.dashboard"))


@caretaker_portal_bp.post("/requests/<int:request_id>/status")
@account_type_required("caretaker")
def status(request_id):
    care_request = db.session.get(CareRequest, request_id)
    care_request.status = request.form["status"]
    care_request.visit_note = request.form.get("visit_note")
    db.session.commit()
    flash("Assignment updated.", "success")
    return redirect(url_for("caretaker_portal.dashboard"))
