from app import db
from datetime import datetime
from helpers import generate_uuid

class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.String(36), default=generate_uuid, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text)

    admins =  db.relationship("ProjectAdmins", backref="project", lazy='dynamic')
    editors =  db.relationship("ProjectEditors", backref="project", lazy='dynamic')
    members =  db.relationship("ProjectMembers", backref="project", lazy='dynamic')

    ports = db.relationship("ProjectDescription", backref="project", lazy='dynamic')

    keywords = db.relationship('Keyword', backref='project', lazy='dynamic')

    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    

    def __repr__(self):
        return '<Project {}>'.format(self.name)