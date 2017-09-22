import os

class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'SOMERANDOMSTRING'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'

class TestConfig(BaseConfig):
    DEBUG = True
    TESTIGN = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # WTF_CSRF_ENABLED = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False
