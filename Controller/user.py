from Controller.common import *


def register_user():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        email = data.get('email')
        address = data.get('address')

        if len(password) < 8 or not re.search("[a-zA-Z]", password) or not re.search("[0-9]", password):
            return jsonify({
                'message': 'Password must be at least 8 characters long and include at least one '
                           'letter and one number'}), 400

        is_email_valid, email_message = validate_email(email)
        if not is_email_valid:
            return jsonify({'message': email_message}), 400

        if User.query.filter_by(Email=email).first():
            return jsonify({'message': 'Email already exists'}), 400

        hashed_password = generate_password_hash(password)
        new_user = User(Username=username, Password=hashed_password, Email=email, Address=address)
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
    user_data = {'username': current_user.Username, 'email': current_user.Email, 'address': current_user.Address,
                 'credit card id': current_user.CreditCardID}
    return jsonify(user_data), 200


def update_user(current_user):
    data = request.get_json()
    user = User.query.filter_by(UserID=current_user.UserID).first()

    if 'username' in data:
        if User.query.filter(User.Username == data['username'], User.UserID != current_user.UserID).first():
            return jsonify({'message': 'Username already taken'}), 400
        user.Username = data['username']

    if 'email' in data:
        is_email_valid, email_message = validate_email(data['email'])
        if not is_email_valid:
            return jsonify({'message': email_message}), 400

        if User.query.filter(User.Email == data['email'], User.UserID != current_user.UserID).first():
            return jsonify({'message': 'Email already exists'}), 400
        user.Email = data['email']

    if 'address' in data:
        user.Address = data['address']

    if 'creditcardID' in data:
        is_credit_card_valid, credit_card_message = validate_credit_card(data['creditcardID'])
        if not is_credit_card_valid:
            return jsonify({'message': credit_card_message}), 400
        user.CreditCardID = data['creditcardID']

    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200
