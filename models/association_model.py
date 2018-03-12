from app import db
from datetime import datetime

## ------------------------ Associations ------------------------ ##

class PortAdmins(db.Model):
    __tablename__ = 'port_admins'
    port_id = db.Column(db.String(36), db.ForeignKey('port.id'), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), primary_key=True)
    approved = db.Column(db.Boolean, default=False)

    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PortEditors(db.Model):
    __tablename__ = 'port_editors'
    port_id = db.Column(db.String(36), db.ForeignKey('port.id'), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), primary_key=True)
    approved = db.Column(db.Boolean, default=False)

    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PortMembers(db.Model):
    __tablename__ = 'port_members'
    port_id = db.Column(db.String(36), db.ForeignKey('port.id'), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), primary_key=True)
    approved = db.Column(db.Boolean, default=False)

    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
