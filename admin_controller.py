import datetime
import jwt
from flask import jsonify, request
from creates_app import creates_app
from models import *


def login_admin():
    data = request.get_json()
    admin_id = data.get('admin_id')
    password = data.get('password')

    admin = Admin.query.filter_by(AdminID=admin_id).first()

    if admin and admin.Password == password:
        token = jwt.encode({
            'admin_id': admin.AdminID,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, creates_app().config['SECRET_KEY'])

        return jsonify({'token': token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401
