from flask_restful import Resource
from models import User, Port
from serializers import user_schema, users_schema, port_schema, ports_schema
from flask import request
from .helpers import POST_DATA, PUT_DATA, DELETE


class UsersViewSet(Resource):
    def get(self):
        return users_schema.dump(User.query.all())
    
    def post(self):
        return POST_DATA(user_schema)

class UserViewSet(Resource):
    def get(self, user_id):
        return user_schema.dump(User.query.get(user_id))
    
    def put(self, user_id):
        return PUT_DATA(user_schema, User, user_id)
    
    def delete(self, user_id):
        return DELETE(User, user_id)

class PortsViewSet(Resource):
    def get(self):
        return ports_schema.dump(Port.query.all())
    
    def post(self):
        return POST_DATA(port_schema)

class PortViewSet(Resource):
    def get(self, port_id):
        return port_schema.dump(Port.query.get(port_id))
    
    def put(self, port_id):
        return PUT_DATA(port_schema, Port, port_id)
    
    def delete(self, port_id):
        return DELETE(Port, port_id)