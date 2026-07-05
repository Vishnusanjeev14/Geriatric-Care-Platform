from flask import Blueprint


caretaker_portal_bp = Blueprint("caretaker_portal", __name__, url_prefix="/caretaker")

from . import routes  # noqa: E402,F401
