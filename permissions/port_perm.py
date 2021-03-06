from flask import jsonify, g

def UserisPortAdmin(fn):
    def wrapper(*args, **kw):
        check = [i for i in g.user.port_admin if i.port.id == kw['port_id']]
        if len(check):
            if check[0].approved:
                return fn(*args, **kw)
            else:
                return jsonify({'message': 'The user admin status is pending for approval'})
        else:
            return jsonify({'message': 'The user is not authorized'})
    return wrapper

def UserisPortEditor(fn):
    def wrapper(*args, **kw):
        if kw['port_id'] in [i.port.id for i in g.user.port_editor]:
            return fn(*args, **kw)
        else:
            return jsonify({'message': 'The user is not authorized'})
    return wrapper
