# controllers.py
from models import *
from sqlalchemy.exc import IntegrityError
from flask import jsonify, request


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
        return jsonify({"message": "Login ok", "user_id": user.UserID}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


def get_products():
    products = Product.query.all()
    products_list = [product.to_dict() for product in products]
    return jsonify(products_list), 200
