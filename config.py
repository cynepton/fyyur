import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://doadmin:adxi23ks43tnh995@testcluster-do-user-8414461-0.b.db.ondigitalocean.com:25060/fsnd?sslmode=require'
SQLALCHEMY_TRACK_MODIFICATIONS=False
