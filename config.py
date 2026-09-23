import os


class Config:
    """Base configuration, values come from environment variables."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


def get_config():
    env = os.environ.get("FLASK_ENV", "production")
    return DevelopmentConfig if env == "development" else ProductionConfig
