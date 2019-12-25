# metrics/utils/config.py
"""Manages config data for the app."""
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
DB_NAME = 'autoupdaterapi'
MONGO_BASEURL = 'mongodb://localhost/'


class BaseConfig:
    """Base configuration."""
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    if SECRET_KEY is None:
        os.environ['SECRET_KEY'] = str(os.urandom(24))
        SECRET_KEY = os.getenv('SECRET_KEY')
    MONGODB_HOST = MONGO_BASEURL + DB_NAME


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    MONGODB_HOST = MONGO_BASEURL + DB_NAME + '_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    # TODO Use credentials to authenticate DB connection.
