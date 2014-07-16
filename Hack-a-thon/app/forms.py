'''
Created on Jul 2, 2014

@author: lan_xu, alvin_yau
'''
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, DateTimeField, IntegerField, validators
from wtforms.validators import Required, Email
from wtforms.validators import ValidationError
from models import User


class LoginForm(Form):
    username = TextField('username', validators = [Required('Email is required'), validators.Email()])
    password = PasswordField('password', validators = [Required('Password is required')])

# @author alvin_yau
class RegisterForm(Form):
    def unique_email(form, field):
        user = User.query.filter_by(username = form.username.data).first()
        if user is not None:
            raise ValidationError('User already exists!')
    
    def retype_password_validate(form, field):
        if form.password.data != form.password2.data: 
            raise ValidationError('Password Must Match!')
    
    username = TextField('username', [Required('Email is required'), Email(), unique_email])
    password = PasswordField('password', validators = [Required('Password is required')])
    password2 = PasswordField('password2', validators = [Required('Please Retype your password'), retype_password_validate])
    first_name = TextField('first_name', validators = [Required('First name is required')])
    last_name = TextField('last_name', validators = [Required('Last name is required')])


class TeamForm(Form):
    teamname = TextField('name', validators = [Required('Team name is required')])
    member = TextField('member')

# @author alvin_yau
class EventForm(Form):
    name = TextField('name', [Required('Name is required')])
    starttime = DateTimeField('name', format='%Y-%m-%dT%H:%M', validators = [Required("Start time is required")])
    endtime = DateTimeField('name', format='%Y-%m-%dT%H:%M', validators = [Required("End time is required")])
    location = TextField('name', [Required('Location is required')])
    max_team = IntegerField('name', [Required('Max Team must be an integer.')])
    max_member_per_team = IntegerField('max_member_per_team', [Required('Max Number Per Team must be an integer')])
    department = TextField('name', [Required('Department is required')])
    description = TextField('name', [Required('Description is required')])

