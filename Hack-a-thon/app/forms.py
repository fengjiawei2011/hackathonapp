'''
Created on Jul 2, 2014

@author: lan_xu
'''
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, DateTimeField, DateField, IntegerField
from wtforms.validators import Required
from datetime import date
from wtforms.validators import ValidationError

class LoginForm(Form):
    username = TextField('username', validators = [Required('Username is required')])
    password = PasswordField('password', validators = [Required('Password is required')])


class RegisterForm(Form):
    def unique_user_name(form, field):
        return
    
    def retype_password_validate(form, field):
        if form.password.data != form.password2.data: 
            raise ValidationError('Password Must Match!')
    
    username = TextField('username', validators = [Required('Username is required'), unique_user_name])
    password = PasswordField('password', validators = [Required('Password is required')])
    password2 = PasswordField('password2', validators = [Required('Please Retype your password'), retype_password_validate])
    
    
