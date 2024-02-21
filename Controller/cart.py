from Controller.common import *


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
