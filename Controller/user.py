from Controller.common import *


def register_user():
    try:
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'])
        new_user = User(Username=data['username'], Password=hashed_password,
                        Email=data.get('email'), Address=data.get('address'))
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Register ok"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Username already exist"}), 400


def login_user():
    data = request.get_json()
    user = User.query.filter_by(Username=data['username']).first()

    if user and check_password_hash(user.Password, data['password']):
        token = jwt.encode({
            'user_id': user.UserID,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
        }, creates_app().config['SECRET_KEY'])

        return jsonify({'token': token}), 200

    else:
        return jsonify({"message": "Invalid username or password"}), 401


def get_user_info(current_user):
    user_data = {'username': current_user.Username, 'email': current_user.Email, 'address': current_user.Address}
    return jsonify(user_data), 200


def update_user(current_user):
    data = request.get_json()
    user = User.query.filter_by(UserID=current_user.UserID).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    if 'username' in data:
        user.Username = data['username']
    if 'email' in data:
        user.Email = data['email']
    if 'address' in data:
        user.Address = data['address']
    if 'creditcardID' in data:
        user.CreditCardID = data['creditcardID']

    db.session.commit()

    return jsonify({'message': 'User updated successfully'}), 200
