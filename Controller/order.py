from Controller.common import *


def create_order(current_user):
    data = request.get_json()
    payment_type = data.get('payment_type')
    credit_card_info = data.get('credit_card_info', None)

    cart = Cart.query.filter_by(UserID=current_user.UserID).first()
    if not cart or len(cart.cartdetails) == 0:
        return jsonify({'message': 'Cart is empty'}), 400

    if payment_type == "CREDIT_CARD":
        if not credit_card_info and not current_user.CreditCardID:
            return jsonify({'message': 'Credit card information is required'}), 400
        if credit_card_info:
            current_user.CreditCardID = credit_card_info
            db.session.commit()

    new_order = Order(
        UserID=current_user.UserID,
        OrderDate=date.today(),
        Status=OrderStatus.PLACED,
        Address=current_user.Address,
        PaymentType=payment_type
    )
    db.session.add(new_order)
    db.session.commit()

    for item in cart.cartdetails:
        order_detail = OrderDetail(
            OrderID=new_order.OrderID,
            ProductID=item.ProductID,
            Quantity=item.Quantity,
            SalePrice=item.product.Price
        )
        db.session.add(order_detail)

        product = Product.query.get(item.ProductID)
        product.StockQuantity -= item.Quantity

    CartDetail.query.filter_by(CartID=cart.CartID).delete()
    db.session.commit()

    return jsonify({'message': 'Order created successfully', 'order_id': new_order.OrderID}), 201
