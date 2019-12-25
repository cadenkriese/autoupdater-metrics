# tests/test_config.py
import pytest
from flask import Flask

generic_app = Flask(__name__)


@pytest.fixture
def setup_dev():
    generic_app.config.from_object('metrics.utils.config.DevelopmentConfig')
    return generic_app


def test_app_is_development(setup_dev):
    app = setup_dev
    assert app.config['SECRET_KEY'] is not None
    assert app.config['DEBUG'] is True
    assert app.config['MONGODB_HOST'] == 'mongodb://localhost/autoupdaterapi'


@pytest.fixture
def setup_testing():
    generic_app.config.from_object('metrics.utils.config.TestingConfig')
    return generic_app


def test_app_is_testing(setup_testing):
    app = setup_testing
    assert app.config['SECRET_KEY'] is not None
    assert app.config['DEBUG'] is True
    assert app.config['TESTING'] is True
    assert app.config['MONGODB_HOST'] == 'mongodb://localhost/autoupdaterapi_test'


@pytest.fixture
def setup_production():
    generic_app.config.from_object('metrics.utils.config.ProductionConfig')
    return generic_app


def test_app_is_production(setup_production):
    app = setup_production
    assert app.config['SECRET_KEY'] is not None
    assert app.config['DEBUG'] is False
    assert app.config['MONGODB_HOST'] == 'mongodb://localhost/autoupdaterapi'
