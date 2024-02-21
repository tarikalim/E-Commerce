from Controller.common import *


def get_products():
    products = Product.query.all()
    products_list = [product.to_dict() for product in products]
    return jsonify(products_list), 200


def get_products_by_category(category_name):
    products = Product.query.join(Category).filter(Category.CategoryName == category_name).all()
    products_list = [product.to_dict() for product in products]
    return jsonify(products_list), 200
