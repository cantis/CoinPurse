from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class BaseConfig(object):
    FLASK_APP = 'wsgi.py'
    # SECRET_KEY = environ.get('SECRET_KEY')
    SECRET_KEY = 'testSecretKeyHere'

    STATIC_FOLDER = 'static'
    TEMPLATE_FOLDER = 'templates'

    FLASK_DEBUG = False
    TESTING = False
    DEBUG = False

    # Database
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(BaseConfig):
    FLASK_ENV = 'production'
    SQLALCHEMY_DATABASE_URI = environ.get('POSTGRES_DATABASE_URI')


class DevConfig(BaseConfig):
    FLASK_ENV = 'development'
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    FLASK_DEBUG = True
    TESTING = True
    DEBUG = True


class TestConfig(BaseConfig):
    ENV = 'testing'
    FLASK_ENV = 'testing'
    FLASK_DEBUG = True
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    LOGIN_DISABLED = True
