from app import db
from geoalchemy2 import Geography
from datetime import datetime
from helpers import generate_uuid

class Port(db.Model):
    __tablename__ = 'port'
    id = db.Column(db.String(36), default=generate_uuid, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    slug = db.Column(db.String(40), unique=True, nullable=False)
    old_slug = db.Column(db.String(40))
    address = db.Column(db.Text)
    description = db.Column(db.Text)
    location = db.Column(Geography(geometry_type='POINT', srid=4326))
    website = db.Column(db.String(60))
    tel = db.Column(db.String(20))
    email = db.Column(db.String(40))
    # logo
    
    admins =  db.relationship("PortAdmins", backref="port", lazy='dynamic')
    editors =  db.relationship("PortEditors", backref="port", lazy='dynamic')
    members =  db.relationship("PortMembers", backref="port", lazy='dynamic')
    
    projects = db.relationship("ProjectDescription", backref="port", lazy='dynamic')

    services = db.relationship('Service', backref='port', lazy='dynamic')

    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Port {}>'.format(self.name)