from flask import Flask
from flask_jwt_extended import JWTManager
from models import db


def creates_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'deneme123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://tarik@34.141.227.97/E-Commerce'

    jwt = JWTManager(app)
    db.init_app(app)

    return app
