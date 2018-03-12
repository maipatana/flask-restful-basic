import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
CORS(app)

db_path = os.path.join(os.path.dirname(__file__), '../database/app.db')
db_uri = 'sqlite:///{}'.format(db_path)

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['ERROR_404_HELP'] = False
app.config['DEBUG'] = True

app.config['SECRET_KEY'] = 'this-is-the-seret-key'

db = SQLAlchemy(app)
ma = Marshmallow(app)

file_handler = RotatingFileHandler('info.log', maxBytes=1024 * 1024 * 100, backupCount=20)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))

app.logger.addHandler(file_handler)
# app.logger.warning('testing warning log')
# app.logger.error('testing error log')
app.logger.info('------------------ STARTING SERVER ------------------')