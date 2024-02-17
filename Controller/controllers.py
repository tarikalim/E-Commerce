import datetime
import jwt
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from creates_app import creates_app
from Model.models import *


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
        return jsonify({'message': 'No authorization'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'No user'}), 404

    user_data = {'username': user.Username, 'email': user.Email, 'address': user.Address}
    return jsonify(user_data), 200


def update_user(current_user):
    data = request.get_json()
    user = User.query.filter_by(UserID=current_user.UserID).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    if 'username' in data:
        user.Username = data['username']
    if 'email' in data:
        user.Email = data['email']
    if 'address' in data:
        user.Address = data['address']
    if 'creditcardID' in data:
        user.CreditCardID = data['creditcardID']

    db.session.commit()

    return jsonify({'message': 'User updated successfully'}), 200


def add_review(current_user, product_id):
    data = request.get_json()
    comment = data['comment']
    rating = data['rating']

    order = Order.query.join(OrderDetail).filter(Order.UserID == current_user.UserID,
                                                 OrderDetail.ProductID == product_id).first()
    if not order:
        return jsonify({'message': 'Not purchased'}), 403

    new_review = Review(UserID=current_user.UserID, ProductID=product_id,
                        Date=datetime.datetime.utcnow(), Comment=comment, Rate=rating)
    db.session.add(new_review)
    db.session.commit()
    return jsonify({'message': 'Review added'}), 201


def get_products():
    products = Product.query.all()
    products_list = [product.to_dict() for product in products]
    return jsonify(products_list), 200


def get_products_by_category(category_name):
    products = Product.query.join(Category).filter(Category.CategoryName == category_name).all()
    products_list = [product.to_dict() for product in products]
    return jsonify(products_list), 200


def add_to_cart(current_user, product_id, quantity):
    product = Product.query.get(product_id)

    if not product or product.StockQuantity < quantity:
        return jsonify({"message": "Product not available or not enough stock"}), 400

    cart = Cart.query.filter_by(UserID=current_user.UserID).first()

    if not cart:
        cart = Cart(UserID=current_user.UserID)
        db.session.add(cart)
        db.session.commit()

    cart_detail = CartDetail.query.filter_by(CartID=cart.CartID, ProductID=product_id).first()
    if cart_detail:
        cart_detail.Quantity += quantity
    else:
        new_cart_detail = CartDetail(CartID=cart.CartID, ProductID=product_id, Quantity=quantity)
        db.session.add(new_cart_detail)

    db.session.commit()
    return jsonify({"message": "Product added to cart"}), 200


def view_cart_details(current_user):
    cart = Cart.query.filter_by(UserID=current_user.UserID).first()

    if not cart:
        return jsonify({'message': 'Cart not found'}), 404

    cart_details = CartDetail.query.filter_by(CartID=cart.CartID).all()

    cart_items = []
    total_price = 0
    for detail in cart_details:
        product = Product.query.get(detail.ProductID)
        if product:
            item = product.to_dict()
            item['quantity'] = detail.Quantity
            item_total_price = product.Price * detail.Quantity
            total_price += item_total_price
            item['total_price'] = str(item_total_price)
            cart_items.append(item)

    return jsonify({'cart_items': cart_items, 'total_cart_price': str(total_price)}), 200
