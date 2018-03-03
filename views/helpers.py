from flask import request, jsonify
from models import db
from sqlalchemy.exc import IntegrityError 
from marshmallow import ValidationError


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
        


