from app import ma
from models import Keyword, Service

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