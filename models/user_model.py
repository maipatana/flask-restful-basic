from app import app, db
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from helpers import generate_uuid

followers = db.Table('followers',
    db.Column('follower_id', db.String(36), db.ForeignKey('user.id')),
    db.Column('following_id', db.String(36), db.ForeignKey('user.id'))
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(36), default=generate_uuid, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    bio = db.Column(db.Text)
    
    port_admin =  db.relationship("PortAdmins", backref="user", lazy='dynamic')
    port_editor =  db.relationship("PortEditors", backref="user", lazy='dynamic')
    port_member =  db.relationship("PortMembers", backref="user", lazy='dynamic')

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
    
    def generate_refresh_token(self, expiration = 36000):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration, salt='refresh-token-salt')
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'], salt='activate-salt')
        try:
            data = s.loads(token)
        except SignatureExpired:
            return 'Token Expired'#None # valid token, but expired
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