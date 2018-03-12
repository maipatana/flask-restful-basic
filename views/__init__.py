from flask import request, jsonify, g
from flask_restful import Resource
from models import User
from permissions.auth import auth
from .port_view import PortViewSet, PortsViewSet
from .user_view import UserViewSet, UsersViewSet

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

