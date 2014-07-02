'''
Created on Jul 2, 2014

@author: lan_xu
'''
from app import sqldb
from werkzeug.security import generate_password_hash, check_password_hash

class User(sqldb.Model):
    id = sqldb.Column(sqldb.Integer, primary_key=True)
    role = sqldb.Column(sqldb.Boolean, nullable=False, default=False)  # True for admin, False for basic user
    username = sqldb.Column(sqldb.String(50), nullable=False, unique=True)
    password = sqldb.Column(sqldb.String(255), nullable=False)
    first_name = sqldb.Column(sqldb.String(255), nullable=True)
    last_name = sqldb.Column(sqldb.String(255), nullable=True)
    events = sqldb.relationship('Event', backref = 'admin', lazy = 'dynamic')
    teams = sqldb.relationship('Team', backref = 'creator', lazy = 'dynamic')
    
    
    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def is_authenticated(self):
        return True
        
    def is_admin(self):
        return self.role
    
    def is_active(self):
        return True
    
    def get_id(self):
        return unicode(self.id)


class Event(sqldb.Model):
    id = sqldb.Column(sqldb.Integer, primary_key=True)
    user_id = sqldb.Column(sqldb.Integer, sqldb.ForeignKey('user.id'), nullable=False)
    name = sqldb.Column(sqldb.String(100), nullable=False)
    description = sqldb.Column(sqldb.String(300), nullable=False)
    starttime = sqldb.Column(sqldb.DateTime)
    endtime = sqldb.Column(sqldb.DateTime)
    location = sqldb.Column(sqldb.String(100), nullable=False)
    max_team = sqldb.Column(sqldb.Integer, nullable=False)
    max_member_per_team = sqldb.Column(sqldb.Integer, nullable=False)
    department = sqldb.Column(sqldb.String(100), nullable=True)
    teams = sqldb.relationship('Team', backref = 'event', lazy = 'dynamic')
    
    
class Team(sqldb.Model):
    id = sqldb.Column(sqldb.Integer, primary_key=True)
    user_id = sqldb.Column(sqldb.Integer, sqldb.ForeignKey('user.id'), nullable=False)
    event_id = sqldb.Column(sqldb.Integer, sqldb.ForeignKey('event.id'), nullable=False)
    name = sqldb.Column(sqldb.String(100), nullable=False)
    members = sqldb.relationship('Member', backref = 'team', lazy = 'dynamic')
    

class Member(sqldb.Model):
    id = sqldb.Column(sqldb.Integer, primary_key=True)
    team_id = sqldb.Column(sqldb.Integer, sqldb.ForeignKey('team.id'), nullable=False)
    member_name = sqldb.Column(sqldb.String(100), nullable=False)
    
    