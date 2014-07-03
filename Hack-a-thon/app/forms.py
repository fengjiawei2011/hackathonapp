'''
Created on Jul 2, 2014

@author: lan_xu, alvin_yau
'''
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, DateTimeField, DateField, IntegerField, validators
from wtforms.validators import Required, Email
from datetime import date
from wtforms.validators import ValidationError
from models import User


class LoginForm(Form):
    username = TextField('username', validators = [Required('Email is required'), validators.Email()])
    password = PasswordField('password', validators = [Required('Password is required')])


class RegisterForm(Form):
    def unique_email(form, field):
        user = User.query.filter_by(username = form.username.data).first()
        if user is not None:
            raise ValidationError('User already exists!')
    
    def retype_password_validate(form, field):
        if form.password.data != form.password2.data: 
            raise ValidationError('Password Must Match!')
    
    username = TextField('username', [Required('Email is required'), validators.Email(), unique_email])
    password = PasswordField('password', validators = [Required('Password is required')])
    password2 = PasswordField('password2', validators = [Required('Please Retype your password'), retype_password_validate])
    first_name = TextField('first_name', validators = [Required('First name is required')])
    last_name = TextField('last_name', validators = [Required('Last name is required')])

class TeamForm(Form):
    teamname = TextField('name', validators = [Required('Team name is required')])
    member = TextField('member')