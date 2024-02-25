from functools import wraps
from flask import request, jsonify
import jwt
from Model.models import User, Admin
from create_app import create_app


def token_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None

            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(" ")[1]

            if not token:
                return jsonify({'message': 'Token is missing!'}), 401

            try:
                data = jwt.decode(token, create_app().config['SECRET_KEY'], algorithms=["HS256"])
            except:
                return jsonify({'message': 'Token is invalid!'}), 401

            if role == 'admin':
                admin = Admin.query.filter_by(AdminID=data.get('admin_id')).first()
                if not admin:
                    return jsonify({'message': 'Admin access required!'}), 401
                return f(*args, **kwargs)
            elif role == 'user' or role is None:
                user = User.query.filter_by(UserID=data.get('user_id')).first()
                if not user:
                    return jsonify({'message': 'User access required!'}), 401
                return f(user, *args, **kwargs)

            return jsonify({'message': 'Invalid role specified!'}), 401

        return decorated_function

    return decorator
