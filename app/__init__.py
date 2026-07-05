from pathlib import Path

from flask import Flask

from config import get_config

from .blueprints.auth import auth_bp
from .blueprints.care import care_bp
from .blueprints.caretaker_portal import caretaker_portal_bp
from .blueprints.errors import errors_bp
from .blueprints.family import family_bp
from .blueprints.healthcare import healthcare_bp
from .blueprints.home_services import home_services_bp
from .blueprints.hospitals import hospitals_bp
from .blueprints.main import main_bp
from .blueprints.ocr import ocr_bp
from .blueprints.pharmacy import pharmacy_bp
from .blueprints.profiles import profiles_bp
from .extensions import csrf, db, migrate
from .logging_config import configure_logging
from .services.auth_service import current_account
from .services.bootstrap import bootstrap_demo_data
from .services.i18n import SUPPORTED_LANGUAGES, translate
from .services.profile_service import active_profile, managed_profiles


def create_app(config_object=None):
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="templates",
        static_folder="static",
    )

    app.config.from_object(config_object or get_config())
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    configure_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_template_context(app)
    register_security_headers(app)

    if app.config.get("AUTO_BOOTSTRAP_DEMO"):
        with app.app_context():
            bootstrap_demo_data()

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(family_bp)
    app.register_blueprint(profiles_bp)
    app.register_blueprint(pharmacy_bp)
    app.register_blueprint(hospitals_bp)
    app.register_blueprint(ocr_bp)
    app.register_blueprint(care_bp)
    app.register_blueprint(home_services_bp)
    app.register_blueprint(healthcare_bp)
    app.register_blueprint(caretaker_portal_bp)
    app.register_blueprint(errors_bp)


def register_template_context(app):
    @app.context_processor
    def inject_context():
        account = current_account()
        profile = active_profile(account.id) if account and account.account_type == "family" else None
        profiles = managed_profiles(account.id) if account and account.account_type == "family" else []
        return {
            "current_account": account,
            "active_profile": profile,
            "managed_profiles": profiles,
            "languages": SUPPORTED_LANGUAGES,
            "t": lambda key: translate(key, account),
        }


def register_security_headers(app):
    @app.after_request
    def add_no_store_headers(response):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
