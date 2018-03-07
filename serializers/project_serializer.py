from app import ma
from models import Project, ProjectAdmins, ProjectEditors, ProjectMembers, ProjectDescription

## ---------------------- Projects ---------------------- ##
class ProjectSchema(ma.ModelSchema):
    class Meta:
        model = Project
        # fields = ('editors', 'id', 'name')
        exclude = ('admins', 'editors')
    # admins = ma.Nested('ProjectAdminsSchema', many=True, only=['user', 'approved'])
    # editors = ma.Nested('ProjectEditorsSchema', many=True, only=['user', 'approved'])
    team = ma.Nested('ProjectMembersSchema', many=True, only=['user', 'approved'])

    ports = ma.Nested('ProjectDescriptionSchema', many=True, only=['description', 'project'])
    keywords = ma.Nested('KeywordSchema', many=True, only=['item'])
    # editors = ma.List(ma.HyperlinkRelated('userviewset', url_key='user_id', external=True))
    # url = ma.URLFor('portviewset', port_id='<id>',  _external=True)

project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)

class ProjectAdminsSchema(ma.ModelSchema):
    class Meta:
        model = ProjectAdmins
    user = ma.Nested('UserSchema', many=False, only=['username', 'id'])

class ProjectEditorsSchema(ma.ModelSchema):
    class Meta:
        model = ProjectEditors
    user = ma.Nested('UserSchema', many=False, only=['username', 'id'])

class ProjectMembersSchema(ma.ModelSchema):
    class Meta:
        model = ProjectMembers
    user = ma.Nested('UserSchema', many=False, only=['username', 'id'])

## ---------------------- ProjectDescription ---------------------- ##
class ProjectDescriptionSchema(ma.ModelSchema):
    class Meta:
        model = ProjectDescription
        # fields = ('editors', 'id', 'name')

    port = ma.Nested('PortSchema', many=False, only=['name', 'id'])
    project = ma.Nested('ProjectSchema', many=False, only=['name', 'id'])
    # editors = ma.List(ma.HyperlinkRelated('userviewset', url_key='user_id', external=True))
    # url = ma.URLFor('portviewset', port_id='<id>',  _external=True)