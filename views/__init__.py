from flask import request, jsonify, g
from flask_restful import Resource
from models import User, Port, Project
from serializers import user_schema, users_schema, project_schema, projects_schema, port_schema, ports_schema
from helpers import POST_DATA, PUT_DATA, DELETE
from permissions import UserisOwner, UserisPortAdmin, UserisPortEditor, UserisProjectAdmin, UserisProjectEditor
from permissions.auth import auth
from .port_view import PortViewSet, PortsViewSet
from .user_view import USER_AUTH, USER_REGISTER


class UsersViewSet(Resource):
    def get(self):
        return users_schema.dump(User.query.all())
    
    def post(self):
        return USER_REGISTER()

class UserViewSet(Resource):
    def get(self, user_id):
        return user_schema.dump(User.query.filter_by(username=user_id).first())
        #return user_schema.dump(User.query.get(user_id))
    
    @auth.login_required
    def put(self, user_id):
        return PUT_DATA(user_schema, User, user_id)
    
    @auth.login_required
    def delete(self, user_id):
        return DELETE(User, user_id)

class ProjectsViewSet(Resource):
    def get(self):
        return projects_schema.dump(Project.query.all())
    
    @auth.login_required
    def post(self):
        if len(g.user.port_admin) == 0:
            return jsonify({'message': 'User has to be admin in at least one Port.'})
        return POST_DATA(project_schema)

class ProjectViewSet(Resource):
    def get(self, project_id):
        return project_schema.dump(Project.query.get(project_id))
    
    @auth.login_required
    @UserisProjectAdmin
    def put(self, project_id):
        return PUT_DATA(project_schema, Project, project_id)
    
    @auth.login_required
    @UserisProjectAdmin
    def delete(self, project_id):
        return DELETE(Project, project_id)

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

