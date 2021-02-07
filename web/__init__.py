from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_toastr import Toastr

from config import DevConfig


# create global objects
bs = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
toastr = Toastr()


def clear_filters():
    """ Clear any filters on the form when we re-load """
    # db.Setting.query.filter_by(key='filter_game_session').delete()


def create_app():
    """ Set up the flask app and initialize global objects """
    # Create the flask application
    app = Flask(__name__)

    # set the configuration
    app.config.from_object(DevConfig())

    # initalize our globlal objects
    bs.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    toastr.init_app(app)

    from web.routes.character import character_bp
    app.register_blueprint(character_bp)

    from web.routes.entry import entry_bp
    app.register_blueprint(entry_bp)

    from web.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app
