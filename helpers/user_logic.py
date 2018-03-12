from flask import request, jsonify, make_response
from app import db
from models import User
from serializers import user_schema

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