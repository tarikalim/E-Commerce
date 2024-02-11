from flask import Flask
from models import db
from controllers import init_app_routes


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://tarik@34.141.227.97/E-Commerce'
    db.init_app(app)
    init_app_routes(app)

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
