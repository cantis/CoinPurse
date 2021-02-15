from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class BaseConfig(object):
    FLASK_APP = 'wsgi.py'
    SECRET_KEY = 'super_secret_key'

    STATIC_FOLDER = 'static'
    TEMPLATE_FOLDER = 'templates'

    FLASK_DEBUG = False
    TESTING = False
    DEBUG = False

    # Database
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(BaseConfig):
    ENV = 'production'
    FLASK_ENV = 'production'
    SQLALCHEMY_DATABASE_URI = environ.get('PROD_DATABASE_URI')


class DevConfig(BaseConfig):
    """ Development Configuration """
    ENV = 'development'
    FLASK_ENV = 'development'
    FLASK_DEBUG = True
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../data/wallet.sqlite'


class TestConfig(BaseConfig):
    """ Testing Configuration """
    ENV = 'testing'
    FLASK_ENV = 'testing'
    FLASK_DEBUG = True
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    LOGIN_DISABLED = True
