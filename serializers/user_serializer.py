from app import ma
from models import User

## ---------------------- Users ---------------------- ##
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        exclude = ['password_hash']
    port_admin = ma.Nested('PortAdminsSchema', many=True, only=['port', 'approved'])
    port_editor = ma.Nested('PortEditorsSchema', many=True, only=['port', 'approved'])
    port_team = ma.Nested('PortMemberSchema', many=True, only=['port', 'approved'])
    project_admin = ma.Nested('ProjectAdminsSchema', many=True, only=['project', 'approved'])
    project_editor = ma.Nested('ProjectEditorsSchema', many=True, only=['project', 'approved'])
    project_team = ma.Nested('ProjectMembersSchema', many=True, only=['project', 'approved'])
    
    followers = ma.Nested('UserSchema', many=True, only=['username', 'id'])
    following = ma.Nested('UserSchema', many=True, only=['username', 'id'])
    # ports = ma.List(ma.HyperlinkRelated('portviewset', url_key='port_id', external=True))

user_schema = UserSchema()
users_schema = UserSchema(many=True)