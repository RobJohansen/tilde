'''App Configuration'''

import os

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    '''SQL Alchemy Configuration'''

    SQLALCHEMY_DATABASE_URI = \
        os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(ROOT_DIR, 'db', 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
