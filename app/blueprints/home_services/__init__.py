from flask import Blueprint


home_services_bp = Blueprint("home_services", __name__, url_prefix="/home-services")

from . import routes  # noqa: E402,F401
