from flask import request, jsonify, g
from models import db, User
from serializers import user_schema
from sqlalchemy.exc import IntegrityError 
from marshmallow import ValidationError

## ---------------------- Operations ---------------------- ##

def POST_DATA(Schema):
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    # Validate and deserialize input
    try:
        data = Schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    try:
        db.session.add(data.data)
        db.session.commit()
    except IntegrityError as exc:
        reason = exc._message().split(':')
        if reason[0].endswith('UNIQUE constraint failed'):
            already_exist = reason[1].split('.')[1]
            # print("%s already exists" % exc.params[1])
            db.session.rollback()
            return jsonify({'message': "already exists", 'field': already_exist, 'value': json_data[already_exist]})
    return Schema.dump(data.data)

def PUT_DATA(Schema, Table, id):
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    # Validate and deserialize input
    ROW_TO_UPDATE = Table.query.get(id)
    if not ROW_TO_UPDATE:
        return jsonify({'message': 'not exists'})
    try:
        data = Schema.load(json_data, instance=ROW_TO_UPDATE)
    except ValidationError as err:
        return jsonify(err.messages), 422
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({'message': 'not success'})
    return Schema.dump(data.data)

def DELETE(Table, id):
    item = Table.query.get(id)
    if not item:
        return jsonify({'message': 'not exists'})
    try:
        db.session.delete(item)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({'message': 'not success'})
    return jsonify({'message': 'success'})


## ---------------------- User Registration ---------------------- ##

def USER_REGISTER():
    json_data = request.get_json()
    username = json_data['username']
    password = json_data['password']
    if username is None or password is None:
        return jsonify({'message': 'No input data provided'}), 400 # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        return jsonify({'message': 'already exists', 'field': 'username', 'value': username}) # existing user
    
    user = User(username = username)
    user.hash_password(password)
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({'message': 'failed'}), 422
    return user_schema.dump(user)

def USER_AUTH():
    # first try to authenticate by token
    auth_token = request.headers.get('Authorization')
    if auth_token:
        user = User.verify_auth_token(auth_token.split(' ')[1])
    else:
        json_data = request.get_json()
        username = json_data['username']
        password = json_data['password']
        if username is None or password is None:
            return jsonify({'message': 'No input data provided'}), 400 # missing arguments
        user = User.query.filter_by(username = username).first()
        if user is not None:
            user = User.query.filter_by(username = username_or_token).first()
            if not user or not user.verify_password(password):
                return False
        else:
            return False
    g.user = user
    return True


