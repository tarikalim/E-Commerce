from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

mail = Mail()
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()