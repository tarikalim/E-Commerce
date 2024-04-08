from flask import Flask
from extensions import *
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from Route import routes
    routes.init_routes(app)
    mail.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    swagger.init_app(app)

    return app
