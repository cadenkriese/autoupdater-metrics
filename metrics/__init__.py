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


@JWT.expired_token_loader
def token_expired(expired_token):
    """
    Informs the user that their token has expired.
    :param expired_token: The expired, but otherwise valid, token.
    :return: A 401 message that their token expired.
    """
    token_type = expired_token['type']
    return {'msg': 'The {} token has expired'.format(token_type)}, 401


if __name__ == "__main__":
    APP.run()
