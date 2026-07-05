import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

DEFAULT_MYSQL_DATABASE_URL = (
    "mysql+pymysql://root:password"
    "@localhost:3306/careconnect_v2?charset=utf8mb4"
)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        DEFAULT_MYSQL_DATABASE_URL,
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    WTF_CSRF_ENABLED = True
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH", 10 * 1024 * 1024))
    AUTO_BOOTSTRAP_DEMO = os.environ.get("AUTO_BOOTSTRAP_DEMO", "true").lower() == "true"


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL", "sqlite:///:memory:")


class ProductionConfig(Config):
    DEBUG = False
    ENV = "production"


CONFIG_BY_NAME = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config():
    config_name = os.environ.get("FLASK_ENV", "development").lower()
    return CONFIG_BY_NAME.get(config_name, DevelopmentConfig)
