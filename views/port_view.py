from flask_restful import Resource
from permissions import UserisPortAdmin, UserisPortEditor
from permissions.auth import auth
from helpers.port_logic import GET_PORTS, GET_PORT, CREATE_PORT, UPDATE_PORT, DELETE_PORT

class PortsViewSet(Resource):
    def get(self):
        return GET_PORTS()
    
    @auth.login_required
    def post(self):
        return CREATE_PORT()

class PortViewSet(Resource):
    def get(self, port_id):
        return GET_PORT(port_id)
    
    @auth.login_required
    @UserisPortAdmin
    def put(self, port_id):
        return UPDATE_PORT(port_id)
    
    @auth.login_required
    @UserisPortAdmin
    def delete(self, port_id):
        return DELETE_PORT(port_id)