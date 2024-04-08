from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

mail = Mail()
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
swagger = Swagger()
