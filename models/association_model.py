from app import db
from datetime import datetime

## ------------------------ Associations ------------------------ ##

class ProjectDescription(db.Model):
    __tablename__ = 'project_description'
    role = db.Column(db.String(80))
    description = db.Column(db.Text)

    port_id = db.Column(db.String(36), db.ForeignKey('port.id'), primary_key=True)
    project_id = db.Column(db.String(36), db.ForeignKey('project.id'), primary_key=True)
    # images
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # def __repr__(self):
    #     return '<ProjectPort {} -> {}>'.format(self.project.name, self.port.name)

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


class ProjectAdmins(db.Model):
    __tablename__ = 'project_admins'
    project_id = db.Column(db.String(36), db.ForeignKey('project.id'), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), primary_key=True)
    approved = db.Column(db.Boolean, default=False)

    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ProjectEditors(db.Model):
    __tablename__ = 'project_editors'
    project_id = db.Column(db.String(36), db.ForeignKey('project.id'), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), primary_key=True)
    approved = db.Column(db.Boolean, default=False)

    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ProjectMembers(db.Model):
    __tablename__ = 'project_members'
    project_id = db.Column(db.String(36), db.ForeignKey('project.id'), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), primary_key=True)
    approved = db.Column(db.Boolean, default=False)

    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)