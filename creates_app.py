from flask import Flask
from flask_jwt_extended import JWTManager
from Model.models import db


def creates_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'deneme123'
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

    JWTManager(app)
    db.init_app(app)

    return app
