from Controller.common import *


def add_review(current_user, product_id):
    data = request.get_json()
    comment = data['comment']
    rating = data['rating']

    order = Order.query.join(OrderDetail).filter(Order.UserID == current_user.UserID,
                                                 OrderDetail.ProductID == product_id).first()
    if not order:
        return jsonify({'message': 'Not purchased'}), 403

    new_review = Review(UserID=current_user.UserID, ProductID=product_id,
                        Date=datetime.datetime.now(datetime.timezone.utc), Comment=comment, Rate=rating)
    db.session.add(new_review)
    db.session.commit()
    return jsonify({'message': 'Review added'}), 201


def get_reviews_for_product(product_id):
    try:
        reviews = Review.query.filter_by(ProductID=product_id).all()
        review_list = []

        for review in reviews:
            review_data = {
                'review_id': review.ReviewID,
                'user_id': review.UserID,
                'product_id': review.ProductID,
                'date': review.Date.strftime("%Y-%m-%d"),
                'comment': review.Comment,
                'rate': review.Rate
            }
            review_list.append(review_data)

        return jsonify({'reviews': review_list}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
