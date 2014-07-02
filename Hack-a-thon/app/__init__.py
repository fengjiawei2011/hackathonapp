'''
Created on Jul 2, 2014

@author: lan_xu
'''
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.login import LoginManager
from sqlalchemy import create_engine


app = Flask(__name__)
app.config.from_object('config')

sqldb = SQLAlchemy(app)
migrate = Migrate(app, sqldb)

dbmanager = Manager(app)
dbmanager.add_command('db', MigrateCommand)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import models, views