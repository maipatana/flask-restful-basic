from flask import request, jsonify, g, make_response
from flask_restful import Resource
from serializers import user_schema, users_schema
from models import User
from helpers import PUT_DATA, DELETE
from helpers.user_logic import USER_REGISTER
from permissions import UserisOwner
from permissions.auth import auth

class UsersViewSet(Resource):
    def get(self):
        return users_schema.dump(User.query.all())
    
    def post(self):
        return USER_REGISTER()

class UserViewSet(Resource):
    def get(self, user_id):
        return user_schema.dump(User.query.get(user_id))
    
    @auth.login_required
    @UserisOwner
    def put(self, user_id):
        return PUT_DATA(user_schema, User, user_id)
    
    @auth.login_required
    @UserisOwner
    def delete(self, user_id):
        return DELETE(User, user_id)

