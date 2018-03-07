from flask import Flask
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
