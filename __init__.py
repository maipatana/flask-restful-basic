from flask_restful import Api
from views import UsersViewSet, UserViewSet, PortsViewSet, PortViewSet, AuthforToken, RefreshToken

from app import app

api = Api(app)

api.add_resource(UsersViewSet, '/api/users/')
api.add_resource(UserViewSet, '/api/user/<user_id>')

api.add_resource(PortsViewSet, '/api/ports/')
api.add_resource(PortViewSet, '/api/port/<port_id>')

api.add_resource(AuthforToken, '/api/token/')
api.add_resource(RefreshToken, '/api/refresh-token/')

if __name__ == '__main__':
    app.run(debug=True)