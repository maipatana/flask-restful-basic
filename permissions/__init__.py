from flask import jsonify, g

def UserisOwner(fn):
    def wrapper(*args, **kw):
        if kw['user_id'] == g.user.id:
            return fn(*args, **kw)
        else:
            return jsonify({'message': 'The user is not authorized'})
    return wrapper

def UserisPortAdmin(fn):
    def wrapper(*args, **kw):
        print(g.user)
        if kw['port_id'] in [i.id for i in g.user.port_admin]:
            return fn(*args, **kw)
        else:
            return jsonify({'message': 'The user is not authorized'})
    return wrapper

def UserisPortEditor(fn):
    def wrapper(*args, **kw):
        if kw['port_id'] in [i.id for i in g.user.port_editor]:
            return fn(*args, **kw)
        else:
            return jsonify({'message': 'The user is not authorized'})
    return wrapper

def UserisProjectAdmin(fn):
    def wrapper(*args, **kw):
        if kw['project_id'] in [i.id for i in g.user.project_admin]:
            return fn(*args, **kw)
        else:
            return jsonify({'message': 'The user is not authorized'})
    return wrapper

def UserisProjectEditor(fn):
    def wrapper(*args, **kw):
        if kw['project_id'] in [i.id for i in g.user.project_editor]:
            return fn(*args, **kw)
        else:
            return jsonify({'message': 'The user is not authorized'})
    return wrapper
