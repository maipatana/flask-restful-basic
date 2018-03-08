import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
CORS(app)

# db_path = os.path.join(os.path.dirname(__file__), '../database/app.db')
# db_uri = 'sqlite:///{}'.format(db_path)
db_uri = 'postgresql+psycopg2://postgres:lc4vLddd946xBuEe@35.189.67.236/testproject'
# db_uri = 'postgresql+psycopg2://testproject:testproject@127.0.0.1:5432/testdb'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['ERROR_404_HELP'] = False
app.config['DEBUG'] = True

app.config['SECRET_KEY'] = 'this-is-the-seret-key-that-I-should-keep-it-secret-without-anyone-to-know-!£$%&*'

db = SQLAlchemy(app)
ma = Marshmallow(app)

# handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
# handler.setLevel(logging.INFO)
# app.logger.addHandler(handler)



file_handler = RotatingFileHandler('python.log', maxBytes=1024 * 1024 * 100, backupCount=20)
#file_handler.setLevel(logging.ERROR)
# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# file_handler.setFormatter(formatter)
# logformat = """
# Request:   {method} {path}
# IP:        {ip}
# User:      {user}
# Agent:     {agent_platform} | {agent_browser} {agent_browser_version}
# Raw Agent: {agent}
#             """.format(
#                 method = request.method,
#                 path = request.path,
#                 ip = request.remote_addr,
#                 agent_platform = request.user_agent.platform,
#                 agent_browser = request.user_agent.browser,
#                 agent_browser_version = request.user_agent.version,
#                 agent = request.user_agent.string,
#                 user=user
#             )

file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))

app.logger.addHandler(file_handler)
# app.logger.warning('testing warning log')
# app.logger.error('testing error log')
app.logger.info('------------------ STARTING SERVER ------------------')