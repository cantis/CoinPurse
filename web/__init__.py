import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_toastr import Toastr
import psycopg2

from config import DevConfig, ProdConfig

# For gunicorn / nginx config
# https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/

# create global objects
bs = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
toastr = Toastr()
login_manager = LoginManager()


def clear_filters():
    """ Clear any filters on the form when we re-load """
    # db.Setting.query.filter_by(key='filter_game_session').delete()


def create_app():
    """ Set up the flask app and initialize global objects """
    # Create the flask application
    app = Flask(__name__)

    # The ENV environment variable is set in the launch.json file and we default here to production.
    environment = os.getenv('ENV', 'prod')

    if environment == 'debug':
        app.config.from_object(DevConfig())

    if environment == 'prod':
        app.config.from_object(ProdConfig())

    # initalize our globlal objects
    bs.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    toastr.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'

    from web.routes.character import character_bp
    app.register_blueprint(character_bp)

    from web.routes.entry import entry_bp
    app.register_blueprint(entry_bp)

    from web.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app
