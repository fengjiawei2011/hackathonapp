#!flask/bin/python
"""
run command:
flask/bin/python db_manager.py db init
flask/bin/python db_manager.py db migrate
flask/bin/python db_manager.py db upgrade
"""
from app import dbmanager

dbmanager.run()
