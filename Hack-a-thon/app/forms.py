'''
Created on Jul 2, 2014

@author: lan_xu
'''
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, DateTimeField, DateField, IntegerField
from wtforms.validators import Required
from datetime import date

class LoginForm(Form):
    username = TextField('username', validators = [Required('Username is required')])
    password = PasswordField('password', validators = [Required('Password is required')])


