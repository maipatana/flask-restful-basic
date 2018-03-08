from app import ma
from models import Keyword

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