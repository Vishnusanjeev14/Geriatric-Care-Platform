from flask import flash, redirect, render_template, request, url_for

from app.extensions import db
from app.models import CareRequest, Caretaker
from app.permissions.decorators import account_type_required
from app.services.auth_service import current_account
from app.services.module_service import create_care_request
from app.services.profile_service import active_profile

from . import care_bp


@care_bp.route("/", methods=["GET", "POST"])
@account_type_required("family")
def requests():
    profile = active_profile(current_account().id)
    if request.method == "POST":
        create_care_request(profile, current_account().id, request.form)
        flash("Care request submitted.", "success")
        return redirect(url_for("care.requests"))
    requests = CareRequest.query.filter_by(profile_id=profile.id).order_by(CareRequest.created_at.desc()).all() if profile else []
    caretakers = Caretaker.query.all()
    return render_template("care/requests.html", requests=requests, caretakers=caretakers)


@care_bp.post("/<int:request_id>/note")
@account_type_required("family")
def note(request_id):
    care_request = db.session.get(CareRequest, request_id)
    care_request.visit_note = request.form["visit_note"]
    db.session.commit()
    flash("Care note updated.", "success")
    return redirect(url_for("care.requests"))
