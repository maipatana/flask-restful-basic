from flask import jsonify, request, make_response
from flask_restful import Api
from views import UsersViewSet, UserViewSet, PortsViewSet, PortViewSet, AuthforToken, RefreshToken
from app import app, db
import traceback

api = Api(app)

api.add_resource(UsersViewSet, '/api/users/')
api.add_resource(UserViewSet, '/api/users/<user_id>')

api.add_resource(PortsViewSet, '/api/ports/')
api.add_resource(PortViewSet, '/api/ports/<port_id>')

api.add_resource(AuthforToken, '/api/token/')
api.add_resource(RefreshToken, '/api/refresh-token/')

@app.errorhandler(404)
def not_exist(exception):
    return make_response(jsonify({'message': 'not exists'}), 404)

@app.errorhandler(Exception)
def exceptions(e):
    tb = traceback.format_exc()
    app.logger.error('5xx INTERNAL SERVER ERROR %s %s %s %s \n%s',
                request.remote_addr,
                request.method,
                request.scheme,
                request.full_path,
                tb)
    return make_response(jsonify({'message': 'error'}), 500)

@app.after_request
def after_request(response):
    # This IF avoids the duplication of registry in the log,
    # since that 500 is already logged via @app.errorhandler.
    if response.status_code != 500:
        app.logger.info('%s %s %s %s %s',
                      response.status,
                      request.remote_addr,
                      request.method,
                      request.scheme,
                      request.full_path)
    else:
        app.logger.error('%s %s %s %s %s',
                      response.status,
                      request.remote_addr,
                      request.method,
                      request.scheme,
                      request.full_path)
    return response

if __name__ == '__main__':
    app.run()