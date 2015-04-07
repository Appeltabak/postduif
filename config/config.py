import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE_URI = os.path.join(_basedir, '../server/database.db')

DEBUG = True
