from app import ma
from models import Port, PortAdmins, PortEditors, PortMembers

## ---------------------- Ports ---------------------- ##
class PortSchema(ma.ModelSchema):
    class Meta:
        model = Port
        # fields = ('editors', 'id', 'name')
        exclude = ('admins', 'editors', 'location')
    # admins = ma.Nested('PortAdminsSchema', many=True, only=['user', 'approved'])
    # editors = ma.Nested('PortEditorsSchema', many=True, only=['user', 'approved'])
    team = ma.Nested('PortMembersSchema', many=True, only=['user', 'approved'])

    projects = ma.Nested('ProjectDescriptionSchema', many=True, only=['description', 'project'])
    services = ma.Nested('ServiceSchema', many=True, only=['item'])
    # editors = ma.List(ma.HyperlinkRelated('userviewset', url_key='user_id', external=True))
    # url = ma.URLFor('portviewset', port_id='<id>',  _external=True)

port_schema = PortSchema()
ports_schema = PortSchema(many=True)

class PortAdminsSchema(ma.ModelSchema):
    class Meta:
        model = PortAdmins
    user = ma.Nested('UserSchema', many=False, only=['username', 'id'])

class PortEditorsSchema(ma.ModelSchema):
    class Meta:
        model = PortEditors
        #fields = ('approved',)
    user = ma.Nested('UserSchema', many=False, only=['username', 'id'])

class PortMembersSchema(ma.ModelSchema):
    class Meta:
        model = PortMembers
    user = ma.Nested('UserSchema', many=False, only=['username', 'id'])