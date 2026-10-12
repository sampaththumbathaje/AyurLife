"""
settings.py
-----------

Central configuration file for AyurLife backend.

All environment-specific and sensitive configuration
should be defined here or loaded via environment variables.
"""

import os


class BaseConfig:
    """
    Base configuration shared across environments.
    """

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "ayurlife-secret-key")
    DEBUG = False

    # MongoDB
    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb://localhost:27017/ayurlife"
    )

    # JWT (for authentication)
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "ayurlife-jwt-secret"
    )

    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 24  # 1 day

    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    MONGO_URI = "mongodb://localhost:27017/ayurlife"



class ProductionConfig(BaseConfig):
    """
    Production configuration.
    """
    DEBUG = False
