import os

from flask import Flask

from metrics.database.db import initialize_db
from metrics.resources.routes import initialize_routes
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

if os.environ['SECRET_KEY'] is None:
    os.environ['SECRET_KEY'] = os.urandom(24)

app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]

app.config['MONGODB_SETTINGS'] = {
    'db': 'autoupdaterapi',
    'host': 'localhost'
}

initialize_db(app)
initialize_routes(api)

if __name__ == "__main__":
    app.run()
