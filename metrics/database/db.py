# metrics/database/db.py
from flask_mongoengine import MongoEngine

db = MongoEngine()


def initialize_db(app):
    """
    Initializes the database connection.
    :param app: The flask app to retrieve database information from.
    """
    db.init_app(app)
