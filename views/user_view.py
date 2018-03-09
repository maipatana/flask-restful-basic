from app import db
from flask import request, jsonify, g, make_response
from serializers import user_schema
from models import User

## ---------------------- User Registration ---------------------- ##

def USER_REGISTER():
    json_data = request.get_json()
    try:
        username = json_data['username']
        password = json_data['password']
    except KeyError:
        return make_response(jsonify({'message': 'No input data provided'}), 400) # missing arguments
    if username is None or password is None:
        return make_response(jsonify({'message': 'No input data provided'}), 400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        return jsonify({'message': 'already exists', 'field': 'username', 'value': username}) # existing user
    
    user = User(username = username)
    user.hash_password(password)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(e)
        return make_response(jsonify({'message': 'failed'}), 422)
    return user_schema.dump(user)

def USER_AUTH():
    # first try to authenticate by token
    auth_token = request.headers.get('Authorization')
    if auth_token:
        user = User.verify_auth_token(auth_token.split(' ')[1])
        if user == "Token Expired":
            return make_response(jsonify({'message': 'No input data provided'}), 400)
    else:
        json_data = request.get_json()
        username = json_data['username']
        password = json_data['password']
        if username is None or password is None:
            return make_response(jsonify({'message': 'No input data provided'}), 400) # missing arguments
        user = User.query.filter_by(username = username).first()
        if user is not None:
            user = User.query.filter_by(username = username_or_token).first()
            if not user or not user.verify_password(password):
                return False
        else:
            return False
    g.user = user
    return True