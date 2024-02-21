from Controller.common import *


def get_categories():
    categories = Category.query.all()
    categories_list = [{'id': category.CategoryID, 'name': category.CategoryName} for category in categories]
    return jsonify(categories_list)
