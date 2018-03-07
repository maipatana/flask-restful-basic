from app import app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import uuid
import os

db = SQLAlchemy(app)
ma = Marshmallow(app)


## ------------------------ Migrations ------------------------ ##
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

## ------------------------ Helpers ------------------------ ##

def generate_uuid():
    return str(uuid.uuid4())

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('following_id', db.Integer, db.ForeignKey('user.id'))
)

## ------------------------ Models ------------------------ ##

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(36), default=generate_uuid, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    bio = db.Column(db.Text)
    port_admin = db.relationship('Port', secondary='port_admins', lazy='subquery', backref=db.backref('admins', lazy=True))
    project_admin = db.relationship('Project', secondary='project_admins', lazy='subquery', backref=db.backref('admins', lazy=True))
    port_editor = db.relationship('Port', secondary='port_editors', lazy='subquery', backref=db.backref('editors', lazy=True))
    project_editor = db.relationship('Project', secondary='project_editors', lazy='subquery', backref=db.backref('editors', lazy=True))
    port_team = db.relationship('Port', secondary='port_team', lazy='subquery', backref=db.backref('team', lazy=True))
    project_team = db.relationship('Project', secondary='project_team', lazy='subquery', backref=db.backref('team', lazy=True))

    following = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.following_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def follow(self, user):
        if not self.is_following(user):
            self.following.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        return self.following.filter(
            followers.c.following_id == user.id).count() > 0

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration = 3600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration, salt='activate-salt')
        return s.dumps({ 'id': self.id })
    
    def generate_refresh_token(self, expiration = 86400):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration, salt='refresh-token-salt')
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'], salt='activate-salt')
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user

    @staticmethod
    def verify_refresh_token(token):
        s = Serializer(app.config['SECRET_KEY'], salt='refresh-token-salt')
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user


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
    # projects = db.relationship('Project', secondary='project_port', lazy='subquery', backref=db.backref('ports', lazy=True))
    projects = db.relationship("ProjectDescription", backref="port", lazy='dynamic')

    services = db.relationship('Service', backref='port', lazy='dynamic')

    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Port {}>'.format(self.name)

class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.String(36), default=generate_uuid, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text)

    ports = db.relationship("ProjectDescription", backref="project", lazy='dynamic')

    keywords = db.relationship('Keyword', backref='project', lazy='dynamic')

    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    

    def __repr__(self):
        return '<Project {}>'.format(self.name)

class Keyword(db.Model):
    __tablename__ = 'keyword'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(40), unique=True)
    project_id = db.Column(db.String(36), db.ForeignKey('project.id'))

    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Keyword {}>'.format(self.item)

class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(40), unique=True)
    port_id = db.Column(db.String(36), db.ForeignKey('port.id'))

    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<Service {}>'.format(self.item)

class ProjectDescription(db.Model):
    __tablename__ = 'project_description'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(80))
    description = db.Column(db.Text)

    port_id = db.Column(db.String(36), db.ForeignKey('port.id'))
    project_id = db.Column(db.String(36), db.ForeignKey('project.id'))
    # images
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<ProjectPort {} -> {}>'.format(self.project.name, self.port.name)


## ------------------------ Many-to-Many ------------------------ ##

port_admins = db.Table('port_admins',
    db.Column('port_id', db.Integer, db.ForeignKey('port.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('approved', db.Boolean, default=False)
)

port_editors = db.Table('port_editors',
    db.Column('port_id', db.Integer, db.ForeignKey('port.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('approved', db.Boolean, default=False)
)

port_team = db.Table('port_team',
    db.Column('port_id', db.Integer, db.ForeignKey('port.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('approved', db.Boolean, default=False)
)

project_admins = db.Table('project_admins',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('approved', db.Boolean, default=False)
)

project_editors = db.Table('project_editors',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('approved', db.Boolean, default=False)
)

project_team = db.Table('project_team',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('approved', db.Boolean, default=False)
)

# followers = db.Table('followers',
#     db.Column('follower_id', db.String(40), db.ForeignKey('user.id'), primary_key=True),
#     db.Column('following_id', db.String(40), db.ForeignKey('user.id'), primary_key=True)
# )

if __name__ == '__main__':
    # $ python __init__.py db init
    # $ python __init__.py db migrate
    # $ python __init__.py db upgrade
    manager.run()