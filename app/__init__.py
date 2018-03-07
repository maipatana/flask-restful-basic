from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

db_path = os.path.join(os.path.dirname(__file__), '../database/app.db')
db_uri = 'sqlite:///{}'.format(db_path)

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['ERROR_404_HELP'] = False

app.config['SECRET_KEY'] = 'this-is-the-seret-key-that-I-should-keep-it-secret-without-anyone-to-know-!£$%&*'
