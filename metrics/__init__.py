# metrics/__init__.py
"""Initializes the Flask application."""
from flask import Flask
from flask_restful import Api

from metrics.database import db
from metrics.resources import routes

APP = Flask(__name__)
API = Api(APP)

APP.config.from_object('metrics.utils.config.DevelopmentConfig')

db.initialize_db(APP)
routes.initialize_routes(API)

if __name__ == "__main__":
    APP.run()
