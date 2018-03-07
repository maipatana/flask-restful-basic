from models import User, Port, Project, Keyword, Service, ProjectDescription
from marshmallow import missing, pre_load
from models import ma


## ---------------------- Serializers ---------------------- ##


## ---------------------- Users ---------------------- ##
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        exclude = ['password_hash']
    port_admin = ma.Nested('PortSchema', many=True, only=['name', 'id'])
    port_editor = ma.Nested('PortSchema', many=True, only=['name', 'id'])
    port_team = ma.Nested('PortSchema', many=True, only=['name', 'id'])
    project_admin = ma.Nested('ProjectSchema', many=True, only=['name', 'id'])
    project_editor = ma.Nested('ProjectSchema', many=True, only=['name', 'id'])
    project_team = ma.Nested('ProjectSchema', many=True, only=['name', 'id'])
    
    followers = ma.Nested('UserSchema', many=True, only=['username', 'id'])
    following = ma.Nested('UserSchema', many=True, only=['username', 'id'])
    # ports = ma.List(ma.HyperlinkRelated('portviewset', url_key='port_id', external=True))

user_schema = UserSchema()
users_schema = UserSchema(many=True)

## ---------------------- Ports ---------------------- ##
class PortSchema(ma.ModelSchema):
    class Meta:
        model = Port
        # fields = ('editors', 'id', 'name')
    admins = ma.Nested('UserSchema', many=True, only=['username', 'id'])
    editors = ma.Nested('UserSchema', many=True, only=['username', 'id'])
    team = ma.Nested('UserSchema', many=True, only=['username', 'id'])

    projects = ma.Nested('ProjectDescriptionSchema', many=True, only=['description', 'project'])
    services = ma.Nested('ServiceSchema', many=True, only=['item'])
    # editors = ma.List(ma.HyperlinkRelated('userviewset', url_key='user_id', external=True))
    # url = ma.URLFor('portviewset', port_id='<id>',  _external=True)

port_schema = PortSchema()
ports_schema = PortSchema(many=True)

## ---------------------- Projects ---------------------- ##
class ProjectSchema(ma.ModelSchema):
    class Meta:
        model = Project
        # fields = ('editors', 'id', 'name')
    admins = ma.Nested('UserSchema', many=True, only=['username', 'id'])
    editors = ma.Nested('UserSchema', many=True, only=['username', 'id'])
    team = ma.Nested('UserSchema', many=True, only=['username', 'id'])

    keywords = ma.Nested('KeywordSchema', many=True, only=['item'])
    # editors = ma.List(ma.HyperlinkRelated('userviewset', url_key='user_id', external=True))
    # url = ma.URLFor('portviewset', port_id='<id>',  _external=True)

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)

## ---------------------- Keywords ---------------------- ##
class KeywordSchema(ma.ModelSchema):
    class Meta:
        model = Keyword
        # fields = ('editors', 'id', 'name')

    projects = ma.Nested('ProjectSchema', many=True, only=['name', 'id'])
    # editors = ma.List(ma.HyperlinkRelated('userviewset', url_key='user_id', external=True))
    # url = ma.URLFor('portviewset', port_id='<id>',  _external=True)

keyword_schema = KeywordSchema()
keywords_schema = KeywordSchema(many=True)

## ---------------------- Services ---------------------- ##
class ServiceSchema(ma.ModelSchema):
    class Meta:
        model = Service
        # fields = ('editors', 'id', 'name')

    ports = ma.Nested('PortSchema', many=True, only=['name', 'id'])
    # editors = ma.List(ma.HyperlinkRelated('userviewset', url_key='user_id', external=True))
    # url = ma.URLFor('portviewset', port_id='<id>',  _external=True)

service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)

## ---------------------- ProjectDescription ---------------------- ##
class ProjectDescriptionSchema(ma.ModelSchema):
    class Meta:
        model = ProjectDescription
        # fields = ('editors', 'id', 'name')

    port = ma.Nested('PortSchema', many=False, only=['name', 'id'])
    project = ma.Nested('ProjectSchema', many=False, only=['name', 'id'])
    # editors = ma.List(ma.HyperlinkRelated('userviewset', url_key='user_id', external=True))
    # url = ma.URLFor('portviewset', port_id='<id>',  _external=True)

service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)

## ---------------------- Authentication Token ---------------------- ##
