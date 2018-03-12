from app import ma, db
from helpers.gis_deserialize import GeoConverter, GeographySerializationField
from models import Port, PortAdmins, PortEditors, PortMembers

## ---------------------- Ports ---------------------- ##
class PortSchema(ma.ModelSchema):
    class Meta:
        model = Port
        fields = ('url', 'name')
        exclude = ('admins', 'editors')
        sqla_session = db.session
        model_converter = GeoConverter
    location = GeographySerializationField(attribute='location')
    team = ma.Nested('PortMembersSchema', many=True, only=['user', 'approved'])
    url = ma.URLFor('portviewset', port_id='<id>',  _external=True)

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