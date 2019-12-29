# metrics/__init__.py
"""Initializes the Flask application."""

from dynaconf import FlaskDynaconf
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from metrics.database import db
from metrics.resources import routes

APP = Flask(__name__)
FlaskDynaconf(APP)

API = Api(APP)
JWT = JWTManager(APP)

db.initialize_db(APP)
routes.initialize_routes(API)

if __name__ == "__main__":
    APP.run()
