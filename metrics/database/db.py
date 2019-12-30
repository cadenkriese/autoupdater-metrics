# metrics/database/db.py
"""Manages MongoEngine instance."""
from flask_mongoengine import MongoEngine

DB = MongoEngine()


def initialize_db(app):
    """
    Initializes the database connection.
    :param app: The flask app to retrieve database information from.
    """
    DB.init_app(app)
