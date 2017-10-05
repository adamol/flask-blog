import os

class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'SOMERANDOMSTRING'
    #  SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/flask_blog'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    # WTF_CSRF_ENABLED = False

class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    DEBUG = True

class ProdConfig(BaseConfig):
    DEBUG = False
