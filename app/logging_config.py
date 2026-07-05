import logging
from logging.config import dictConfig


def configure_logging(app):
    log_level = app.config.get("LOG_LEVEL", "INFO")

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                    "formatter": "default",
                }
            },
            "root": {"level": log_level, "handlers": ["console"]},
        }
    )

    app.logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
