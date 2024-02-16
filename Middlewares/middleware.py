from functools import wraps
from flask import request, jsonify
import jwt
from Model.models import User, Admin
from creates_app import creates_app


def user_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, creates_app().config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(UserID=data['user_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated_function


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, creates_app().config['SECRET_KEY'], algorithms=["HS256"])
            admin = Admin.query.filter_by(AdminID=data['admin_id']).first()
            if not admin:
                return jsonify({'message': 'Token is invalid!'}), 401
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(admin, *args, **kwargs)

    return decorated
