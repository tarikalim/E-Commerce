from flask import jsonify, request
from models import User, db
from sqlalchemy.exc import IntegrityError


def init_app_routes(app):
    @app.route('/register', methods=['POST'])
    def register():
        try:
            data = request.get_json()
            new_user = User(Username=data['username'], Password=data['password'], Email=data.get('email'),
                            Address=data.get('address'))
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "Register ok"}), 201

        except IntegrityError:
            db.session.rollback()
            return jsonify({"message": "Invalid username"}), 400

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        user = User.query.filter_by(Username=data['username']).first()
        if user and user.Password == data['password']:
            return jsonify({"message": "Login ok", "user_id": user.UserID}), 200
        else:
            return jsonify({"message": "Invalid"}), 401
