from math import asin, cos, radians, sin, sqrt

from flask import flash, redirect, render_template, request, url_for

from app.models import Appointment, Hospital
from app.permissions.decorators import account_type_required
from app.services.auth_service import current_account
from app.services.module_service import create_appointment
from app.services.profile_service import active_profile

from . import hospitals_bp


@hospitals_bp.route("/", methods=["GET", "POST"])
@account_type_required("family")
def list_hospitals():
    profile = active_profile(current_account().id)
    if request.method == "POST":
        create_appointment(profile, current_account().id, request.form)
        flash("Appointment requested.", "success")
        return redirect(url_for("hospitals.appointments"))
    query = request.args.get("q", "")
    user_lat = request.args.get("lat", type=float)
    user_lon = request.args.get("lon", type=float)
    location_disabled = not (user_lat and user_lon)
    if location_disabled:
        user_lat, user_lon = 13.0827, 80.2707
    hospitals_query = Hospital.query
    if query:
        hospitals_query = hospitals_query.filter(Hospital.name.ilike(f"%{query}%") | Hospital.departments.ilike(f"%{query}%"))
    hospitals = hospitals_query.all()
    hospital_cards = []
    for hospital in hospitals:
        distance = _distance_km(user_lat, user_lon, float(hospital.latitude or 13.0827), float(hospital.longitude or 80.2707))
        hospital_cards.append({"hospital": hospital, "distance": distance, "travel_time": max(5, round(distance * 4))})
    hospital_cards.sort(key=lambda item: item["distance"])
    return render_template("hospitals/list.html", hospital_cards=hospital_cards, query=query, location_disabled=location_disabled, user_lat=user_lat, user_lon=user_lon)


@hospitals_bp.get("/appointments")
@account_type_required("family")
def appointments():
    profile = active_profile(current_account().id)
    appointments = Appointment.query.filter_by(profile_id=profile.id).order_by(Appointment.appointment_date.desc()).all() if profile else []
    return render_template("hospitals/appointments.html", appointments=appointments)


def _distance_km(lat1, lon1, lat2, lon2):
    radius = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return round(2 * radius * asin(sqrt(a)), 1)
