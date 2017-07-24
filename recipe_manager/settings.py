# -*- coding: utf-8 -*-
"""Application configuration."""
import os


class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get('SECRET_KEY', 'TESTSTS')

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', None)

    CELERY_BACKEND = os.environ.get('CELERY_BACKEND', None)
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', None)

    GOOGLE_CONSUMER_KEY = os.environ.get('GOOGLE_CONSUMER_KEY', None)
    GOOGLE_CONSUMER_SECRET = os.environ.get('GOOGLE_CONSUMER_SECRET', None)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = 'DEBUG'
    DEBUG = True


class ProdConfig(Config):
    """Production configuration."""

    ENV = os.environ.get('ENV', 'production')
    LOG_LEVEL = 'INFO'
    DEBUG = False


class DevConfig(Config):
    """Development configuration."""

    ENV = os.environ.get('ENV', 'development')


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    BCRYPT_LOG_ROUNDS = 4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
