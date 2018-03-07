from flask import request, jsonify, g
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from models import User, Port
from serializers import user_schema, users_schema, port_schema, ports_schema
from helpers import POST_DATA, PUT_DATA, DELETE, USER_REGISTER
from permissions import UserisPortAdmin

auth = HTTPBasicAuth()


class UsersViewSet(Resource):
    def get(self):
        return users_schema.dump(User.query.all())
    
    def post(self):
        return USER_REGISTER()

class UserViewSet(Resource):
    def get(self, user_id):
        return user_schema.dump(User.query.get(user_id))
    
    @auth.login_required
    def put(self, user_id):
        return PUT_DATA(user_schema, User, user_id)
    
    @auth.login_required
    def delete(self, user_id):
        return DELETE(User, user_id)

class PortsViewSet(Resource):
    def get(self):
        return ports_schema.dump(Port.query.all())
    
    @auth.login_required
    def post(self):
        return POST_DATA(port_schema)

class PortViewSet(Resource):
    def get(self, port_id):
        return port_schema.dump(Port.query.get(port_id))
    
    @auth.login_required
    @UserisPortAdmin
    def put(self, port_id):
        return PUT_DATA(port_schema, Port, port_id)
    
    @auth.login_required
    @UserisPortAdmin
    def delete(self, port_id):
        return DELETE(Port, port_id)


## ------------------------ Authentication and Token ------------------------ ##

class RefreshToken(Resource):
    def post(self):
        refresh_token = request.headers.get('Authorization')
        if refresh_token:
            user = User.verify_refresh_token(refresh_token.split(' ')[1])
            if user:
                g.user = user
                access_token = g.user.generate_auth_token()
                refresh_token = g.user.generate_refresh_token()
                return jsonify({ 'access_token': access_token.decode('ascii'), 
                    'refresh_token': refresh_token.decode('ascii'),
                    'username': g.user.username })
        return None

class AuthforToken(Resource):
    @auth.login_required
    def post(self):
        access_token = g.user.generate_auth_token()
        refresh_token = g.user.generate_refresh_token()
        return jsonify({ 'access_token': access_token.decode('ascii'), 
            'refresh_token': refresh_token.decode('ascii'),
            'username': g.user.username })

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