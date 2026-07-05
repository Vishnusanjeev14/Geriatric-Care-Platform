from flask import flash, redirect, render_template, request, url_for

from app.models import HomeServiceBooking
from app.permissions.decorators import account_type_required
from app.services.auth_service import current_account
from app.services.module_service import create_home_service
from app.services.profile_service import active_profile

from . import home_services_bp


@home_services_bp.route("/", methods=["GET", "POST"])
@account_type_required("family")
def services():
    profile = active_profile(current_account().id)
    if request.method == "POST":
        create_home_service(profile, current_account().id, request.form)
        flash("Home service requested.", "success")
        return redirect(url_for("home_services.services"))
    bookings = HomeServiceBooking.query.filter_by(profile_id=profile.id).order_by(HomeServiceBooking.created_at.desc()).all() if profile else []
    service_types = ["Cleaning", "Cooking", "Laundry", "Electrician", "Plumber", "Gardener", "Salon", "Appliance Repair"]
    return render_template("home_services/services.html", bookings=bookings, service_types=service_types)
