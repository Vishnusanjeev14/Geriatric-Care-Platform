from flask import Blueprint


care_bp = Blueprint("care", __name__, url_prefix="/care")

from . import routes  # noqa: E402,F401
