from flask import jsonify, g

def UserisOwner(fn):
    def wrapper(*args, **kw):
        if kw['user_id'] == g.user.id:
            return fn(*args, **kw)
        else:
            return jsonify({'message': 'The user is not authorized'})
    return wrapper