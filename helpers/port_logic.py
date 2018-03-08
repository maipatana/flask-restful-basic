from flask import request, jsonify, g, make_response
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from app import app, db
from models import Port, PortAdmins, PortEditors, PortMembers
from serializers import port_schema, ports_schema

## ---------------------- Operations ---------------------- ##

def handeling_commit(data, json_data, operation):
    try:
        db.session.commit()
    except IntegrityError as exc:
        reason = str(exc._message)
        app.logger.error('{} ERROR {}'.format(operation, reason))
        if "duplicate key value" in reason:
            db.session.rollback()
            already_exist = reason.split('Key (')[1]
            already_exist = already_exist.split(')')[0]
            return make_response(jsonify({'message': "already exists", 'field': already_exist, 'value': json_data[already_exist]}), 500)
        else:
            print(exc._message)
            return make_response(jsonify({'message': 'not success'}), 500)
    app.logger.info('{} {} SUCCESS'.format(operation, data.data.id))
    return port_schema.dump(data.data)

def GET_PORTS():
    return ports_schema.dump(Port.query.all())#.filter_by(active=True).all())

def GET_PORT(id):
    item = Port.query.get(id)
    if not item:
        return make_response(jsonify({'message': 'not exists'}), 404)
    return port_schema.dump(item)

def CREATE_PORT():
    json_data = request.get_json()
    app.logger.info('CREATE PORT from USERID {} USERNAME {}'.format(g.user.id, g.user.username))
    if not json_data:
        return make_response(jsonify({'message': 'No input data provided'}), 400)
    data = port_schema.load(json_data)
    if data.errors:
        app.logger.error('{}'.format(data.errors))
        return make_response(jsonify({'message': 'Invalid Data', 'field': list(data.errors.keys())}), 422)
    admin = PortAdmins(user = g.user)
    editor = PortEditors(user = g.user)
    admin.approved = True
    editor.approved = True
    data.data.admins.append(admin)
    data.data.editors.append(editor)
    db.session.add(data.data)
    return handeling_commit(data, json_data, "CREATE PORT")


def UPDATE_PORT(id):
    json_data = request.get_json()
    app.logger.info('UPDATE PORT {} from USERID {}'.format(id, g.user.id, g.user.username))
    if not json_data:
        return make_response(jsonify({'message': 'No input data provided'}), 400)
    # Validate and deserialize input
    ROW_TO_UPDATE = Port.query.get(id)
    if not ROW_TO_UPDATE:
        return make_response(jsonify({'message': 'not exists'}), 404)
    data = port_schema.load(json_data, instance=ROW_TO_UPDATE)
    if data.errors:
        app.logger.error('{}'.format(data.errors))
        return make_response(jsonify({'message': 'Invalid Data', 'field': list(data.errors.keys())}), 422)
    return handeling_commit(data, json_data, "UPDATE PORT")

def DELETE_PORT(id):
    item = Port.query.get(id)
    app.logger.info('DEACTIVATE PORT {}'.format(id))
    if not item:
        return make_response(jsonify({'message': 'not exists'}), 404)
    if not item.active:
        return make_response(jsonify({'message': 'Port is deactive'}), 400)
    num = len(Port.query.filter_by(slug=item.old_slug).all())
    item.deactivate_port("old-slug-" + item.slug + "-" + str(num))
    db.session.commit()
    app.logger.info('DEACTIVATE PORT {} SUCCESS'.format(id))
    return jsonify({'message': 'success'})

def ACTIVATE_PORT(id):
    item = Port.query.get(id)
    app.logger.info('ACTIVATE PORT {}'.format(id))
    if not item:
        return make_response(jsonify({'message': 'not exists'}), 404)
    if item.active:
        return make_response(jsonify({'message': 'Port is active'}), 400)
    num = len(Port.query.filter_by(slug=item.old_slug).all())
    item.activate_port(item.old_slug + "-" + str(num))
    db.session.commit()
    app.logger.info('ACTIVATE PORT {} SUCCESS'.format(id))
    return jsonify({'message': 'success'})