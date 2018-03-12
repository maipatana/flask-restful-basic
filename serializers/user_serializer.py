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
    
    followers = ma.Nested('UserSchema', many=True, only=['username', 'id'])
    following = ma.Nested('UserSchema', many=True, only=['username', 'id'])

user_schema = UserSchema()
users_schema = UserSchema(many=True)