from flask import request, g
from flask_httpauth import HTTPBasicAuth
from models import User

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    # first try to authenticate by token
    auth_token = request.headers.get('Authorization')
    if auth_token:
        user = User.verify_auth_token(auth_token.split(' ')[1])
        if not user:
            return False
    else:
        # try to authenticate with username/password
        json_data = request.get_json()
        try:
            username = json_data['username']
            password = json_data['password']
        except KeyError:
            return False
        if username is None or password is None:
            return False
        user = User.query.filter_by(username = username).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True