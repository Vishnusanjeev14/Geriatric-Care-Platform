from flask import Blueprint


hospitals_bp = Blueprint("hospitals", __name__, url_prefix="/hospitals")

from . import routes  # noqa: E402,F401
