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

    @app.route('/user/<int:user_id>', methods = ['GET'])
    @token_required
    def see_user_info(current_user, user_id):
        return controllers.get_user_info(current_user, user_id)

    @app.route('/products', methods=['GET'])
    @token_required
    def see_products(current_user):
        return controllers.get_products()

