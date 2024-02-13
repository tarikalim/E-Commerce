# routes.py
import controllers
from middleware import token_required


def init_routes(app):
    @app.route('/register', methods=['POST'])
    def register():
        return controllers.register_user()

    @app.route('/login', methods=['POST'])
    def login():
        return controllers.login_user()

    @app.route('/user/<int:user_id>', methods=['GET'])
    @token_required
    def see_user_info(current_user, user_id):
        return controllers.get_user_info(current_user, user_id)

    @app.route('/products', methods=['GET'])
    def see_products():
        return controllers.get_products()

    @app.route('/products/category/<string:category_name>', methods=['GET'])
    def get_products_by_category(category_name):
        return controllers.get_products_by_category(category_name)

    @app.route('/add_review/<int:product_id>', methods=['POST'])
    @token_required
    def add_review_to_product(current_user, product_id):
        return controllers.add_review(current_user, product_id)

