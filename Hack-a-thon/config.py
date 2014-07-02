'''
Created on Jul 2, 2014

@author: lan_xu
'''

import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@10.72.113.193:7111/hackathon'

