from flask import Blueprint


ocr_bp = Blueprint("ocr", __name__, url_prefix="/ocr")

from . import routes  # noqa: E402,F401
