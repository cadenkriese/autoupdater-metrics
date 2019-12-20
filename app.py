from flask import Flask

from database.db import initialize_db
from resources.routes import initialize_routes
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

app.config['MONGODB_SETTINGS'] = {
    'db': 'autoupdaterapi',
    'host': 'localhost'
}

initialize_db(app)
initialize_routes(api)

if __name__ == "__main__":
    app.run()
