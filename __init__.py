from flask import Flask
from flask_restful import Api
from views import UsersViewSet, UserViewSet, PortsViewSet, PortViewSet

app = Flask(__name__)
api = Api(app)

api.add_resource(UsersViewSet, '/users')
api.add_resource(UserViewSet, '/user/<user_id>')

api.add_resource(PortsViewSet, '/ports')
api.add_resource(PortViewSet, '/port/<port_id>')

if __name__ == '__main__':
    app.run(debug=True)