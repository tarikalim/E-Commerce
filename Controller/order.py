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


def get_user_orders(current_user):
    try:
        orders = Order.query.filter_by(UserID=current_user.UserID).all()
        orders_list = []

        for order in orders:
            order_data = {
                'order_id': order.OrderID,
                'order_date': order.OrderDate.strftime("%Y-%m-%d"),
                'status': order.Status.value}
            orders_list.append(order_data)

        return jsonify({'orders': orders_list}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_user_order_details(current_user, order_id):
    try:
        order = Order.query.filter_by(OrderID=order_id, UserID=current_user.UserID).first()
        if not order:
            return jsonify({'message': 'Order not found or access denied'}), 404

        order_details = OrderDetail.query.filter_by(OrderID=order_id).all()
        details_list = []
        total_cost = 0

        for detail in order_details:
            sale_price = float(detail.SalePrice)
            quantity = detail.Quantity
            total_price = sale_price * quantity
            total_cost += total_price

            detail_data = {
                'product_id': detail.ProductID,
                'quantity': quantity,
                'sale_price': sale_price,
                'total_price': total_price
            }
            details_list.append(detail_data)

        return jsonify({'order_details': details_list, 'total_cost': total_cost}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def cancel_user_order(current_user, order_id):
    try:
        order = Order.query.filter_by(OrderID=order_id, UserID=current_user.UserID).first()
        if not order:
            return jsonify({'message': 'Order not found or not authorized to cancel this order'}), 404

        if order.Status == OrderStatus.PLACED:
            order.Status = OrderStatus.CANCELLED
            db.session.commit()
            return jsonify({'message': 'Order cancelled successfully'}), 200
        else:
            return jsonify({'message': 'Order cannot be cancelled because order is:' + order.Status.value}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500
