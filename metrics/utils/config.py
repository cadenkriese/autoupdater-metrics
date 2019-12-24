# project/server/config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))
database_name = 'autoupdaterapi'
mongodb_base = 'mongodb://localhost/'


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    DEBUG = False
    MONGODB_SETTINGS = {
        'host': mongodb_base + database_name
    }


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    MONGODB_SETTINGS = {
        'host': mongodb_base + database_name
    }


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    MONGODB_SETTINGS = {
        'host': mongodb_base + database_name + "_test"
    }
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'my_precious'
    DEBUG = False
    MONGODB_SETTINGS = {
        'host': mongodb_base + database_name
    }
