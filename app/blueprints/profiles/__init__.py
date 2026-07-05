from flask import Blueprint


profiles_bp = Blueprint("profiles", __name__, url_prefix="/profiles")

from . import routes  # noqa: E402,F401
