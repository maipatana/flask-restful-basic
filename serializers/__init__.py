from flask_marshmallow import Marshmallow
from models import User, Port
from marshmallow import missing, pre_load

ma = Marshmallow()

## ---------------------- Serializers ---------------------- ##

## ---------------------- Users ---------------------- ##
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
    ports = ma.Nested('PortSchema', many=True, exclude=['editors'])
    # ports = ma.List(ma.HyperlinkRelated('portviewset', url_key='port_id', external=True))

user_schema = UserSchema()
users_schema = UserSchema(many=True)

## ---------------------- Ports ---------------------- ##
class PortSchema(ma.ModelSchema):
    class Meta:
        model = Port
        fields = ('editors', 'id', 'name')

    editors = ma.Nested(UserSchema, many=True, exclude=['ports', 'bio'])
    # editors = ma.List(ma.HyperlinkRelated('userviewset', url_key='user_id', external=True))
    # url = ma.URLFor('portviewset', port_id='<id>',  _external=True)

port_schema = PortSchema()
ports_schema = PortSchema(many=True)
