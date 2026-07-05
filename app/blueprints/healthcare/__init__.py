from flask import Blueprint


healthcare_bp = Blueprint("healthcare", __name__, url_prefix="/healthcare")

from . import routes  # noqa: E402,F401
