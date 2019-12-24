import unittest

from flask_testing import TestCase
from flask import current_app

from metrics.core import app


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('metrics.utils.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'my_precious')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['MONGODB_HOST'] == 'mongodb://localhost/autoupdaterapi_test'
        )


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('metrics.utils.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'my_precious')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(
            app.config['MONGODB_HOST'] == 'mongodb://localhost/autoupdaterapi_test'
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('metrics.utils.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()
