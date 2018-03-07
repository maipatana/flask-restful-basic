from flask_restful import Resource
from models import Port
from serializers import port_schema, ports_schema
from permissions import UserisPortAdmin, UserisPortEditor
from permissions.auth import auth
from helpers.port_view import CREATE_PORT, UPDATE_PORT, DELETE_PORT

class PortsViewSet(Resource):
    def get(self):
        return ports_schema.dump(Port.query.all())
    
    @auth.login_required
    def post(self):
        return CREATE_PORT()
        #return POST_DATA(port_schema)

class PortViewSet(Resource):
    def get(self, port_id):
        return port_schema.dump(Port.query.get(port_id))
    
    @auth.login_required
    @UserisPortAdmin
    def put(self, port_id):
        return UPDATE_PORT(port_id)
    
    @auth.login_required
    @UserisPortAdmin
    def delete(self, port_id):
        return DELETE_PORT(port_id)