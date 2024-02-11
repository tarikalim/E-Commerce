# routes.py
import controllers

def init_routes(app):
    @app.route('/register', methods=['POST'])
    def register():
        return controllers.register_user()

    @app.route('/login', methods=['POST'])
    def login():
        return controllers.login_user()

