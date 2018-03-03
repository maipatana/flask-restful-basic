from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_marshmallow import Marshmallow
import os
import uuid

db_path = os.path.join(os.path.dirname(__file__), '../database/app.db')
db_uri = 'sqlite:///{}'.format(db_path)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

## ------------------------ Migrations ------------------------ ##
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

## ------------------------ Helpers ------------------------ ##

def generate_uuid():
    return str(uuid.uuid4())

ports = db.Table('ports',
    db.Column('port_id', db.Integer, db.ForeignKey('port.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

## ------------------------ Models ------------------------ ##

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(36), default=generate_uuid, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.Text)
    # postadmin = db.Column()
    # projectadmin = db.Column()
    ports = db.relationship('Port', secondary=ports, lazy='subquery', backref=db.backref('editors', lazy=True))
    # projects = db.Column()

    def __repr__(self):
        return '<User %r>' % self.username


class Port(db.Model):
    __tablename__ = 'port'
    id = db.Column(db.String(36), default=generate_uuid, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    # slug = db.Column(db.String(30), unique=True, nullable=False)
    # address = db.Column()
    # description = db.Column()
    # location = db.Column()
    # website = db.Column()
    # tel = db.Column()
    # email = db.Column()
    # admins = db.Column()
    # services = db.Column()
    # projects = db.Column()
    # keywords = db.Column()

    def __repr__(self):
        return '<Port %r>' % self.name

# class Project(db.Model):
#     pass

# class Keyword(db.Model):
#     pass

# class Service(db.Model):
#     pass

if __name__ == '__main__':
    # $ python __init__.py db init
    # $ python __init__.py db migrate
    # $ python __init__.py db upgrade
    manager.run()