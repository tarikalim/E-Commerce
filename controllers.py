import datetime
import jwt
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from creates_app import creates_app
from models import *


def register_user():
    try:
        data = request.get_json()
        new_user = User(Username=data['username'], Password=data['password'], Email=data.get('email'),
                        Address=data.get('address'))
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Register ok"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Username already exist"}), 400


def login_user():
    data = request.get_json()
    user = User.query.filter_by(Username=data['username']).first()

    if user and user.Password == data['password']:
        token = jwt.encode({
            'user_id': user.UserID,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, creates_app().config['SECRET_KEY'])

        return jsonify({'token': token}), 200

    else:
        return jsonify({"message": "Invalid username or password"}), 401


def get_user_info(current_user, user_id):
    if current_user.UserID != user_id:
        return jsonify({'message': 'login to system'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'No user'}), 404

    user_data = {'username': user.Username, 'email': user.Email, 'address': user.Address}
    return jsonify(user_data), 200

def get_products():
    products = Product.query.all()
    products_list = [product.to_dict() for product in products]
    return jsonify(products_list), 200
