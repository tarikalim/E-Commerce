from Controller import admin, cart, category, order, product, review, user
from Middlewares.middleware import *


def init_routes(app):
    @app.route('/register', methods=['POST'])
    def register():
        return user.register_user()

    @app.route('/user_login', methods=['POST'])
    def login():
        return user.login_user()

    @app.route('/user', methods=['GET'])
    @user_token_required
    def see_user_info(current_user):
        return user.get_user_info(current_user)

    @app.route('/update_user', methods=['PUT'])
    @user_token_required
    def update_user(current_user):
        return user.update_user(current_user)

    @app.route('/products', methods=['GET'])
    def see_products():
        return product.get_products()

    @app.route('/categories', methods=['GET'])
    def get_categories():
        return category.get_categories()

    @app.route('/products/category/<string:category_name>', methods=['GET'])
    def get_products_by_category(category_name):
        return product.get_products_by_category(category_name)

    @app.route('/add_review/<int:product_id>', methods=['POST'])
    @user_token_required
    def add_review_to_product(current_user, product_id):
        return review.add_review(current_user, product_id)

    @app.route('/add_to_cart/<int:product_id>/<int:quantity>', methods=['POST'])
    @user_token_required
    def add_product_to_cart(current_user, product_id, quantity):
        return cart.add_to_cart(current_user, product_id, quantity)

    @app.route('/view_cart', methods=['GET'])
    @user_token_required
    def get_cart_details(current_user):
        return cart.view_cart_details(current_user)

    @app.route('/create_order', methods=['POST'])
    @user_token_required
    def create_order(current_user):
        return order.create_order(current_user)

    @app.route('/reviews/<int:product_id>', methods=['GET'])
    def product_reviews(product_id):
        return review.get_reviews_for_product(product_id)

    @app.route('/admin_login', methods=['POST'])
    def admin_login():
        return admin.login_admin()