from flask import request, jsonify, g
from sqlalchemy.exc import IntegrityError
from app import db
from models import Port, PortAdmins, PortEditors, PortMembers
from serializers import port_schema

## ---------------------- Operations ---------------------- ##

def CREATE_PORT():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    # Validate and deserialize input
    try:
        data = port_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422
    try:
        admin = PortAdmins(user = g.user)
        editor = PortEditors(user = g.user)
        admin.approved = True
        editor.approved = True
        data.data.admins.append(admin)
        data.data.editors.append(editor)
    except Exception as e:
        print(e)
        return jsonify({'message': 'not success'})
    try:
        db.session.add(data.data)
        db.session.commit()
    except IntegrityError as exc:
        # reason = exc._message().split(':')
        # if reason[0].endswith('UNIQUE constraint failed'):
        #     already_exist = reason[1].split('.')[1]
        #     # print("%s already exists" % exc.params[1])
        #     db.session.rollback()
        #     return jsonify({'message': "already exists", 'field': already_exist, 'value': json_data[already_exist]})
        # else:
        #     print(exc._message)
        #     return jsonify({'message': 'not success'})
        reason = str(exc._message)
        if "duplicate key value" in reason:
            db.session.rollback()
            already_exist = reason.split('Key (')[1]
            already_exist = already_exist.split(')')[0]
            return jsonify({'message': "already exists", 'field': already_exist, 'value': json_data[already_exist]})
        else:
            print(exc._message)
            return jsonify({'message': 'not success'})
    return port_schema.dump(data.data)

def UPDATE_PORT(id):
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    # Validate and deserialize input
    ROW_TO_UPDATE = Port.query.get(id)
    if not ROW_TO_UPDATE:
        return jsonify({'message': 'not exists'})
    try:
        data = port_schema.load(json_data, instance=ROW_TO_UPDATE)
    except ValidationError as err:
        return jsonify(err.messages), 422
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({'message': 'not success'})
    return port_schema.dump(data.data)

def DELETE_PORT(id):
    item = Port.query.get(id)
    if not item:
        return jsonify({'message': 'not exists'})
    try:
        item.active = False
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({'message': 'not success'})
    return jsonify({'message': 'success'})