from app import db
from datetime import datetime

class Keyword(db.Model):
    __tablename__ = 'keyword'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(40), unique=True)
    project_id = db.Column(db.String(36), db.ForeignKey('project.id'))

    def __repr__(self):
        return '<Keyword {}>'.format(self.item)

class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(40), unique=True)
    port_id = db.Column(db.String(36), db.ForeignKey('port.id'))

    def __repr__(self):
        return '<Service {}>'.format(self.item)