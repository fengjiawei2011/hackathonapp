#!flask/bin/python
from app.models import User
from app import app, sqldb

# add user
def add_user(name, pwd):
    user = User(username=name, password=pwd)
    sqldb.session.add(user)
    sqldb.session.commit()