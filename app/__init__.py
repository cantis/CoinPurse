from flask import Flask
from flask_bootstrap import Bootstrap
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy

# create global objects
bs = Bootstrap()
db = SQLAlchemy()


def clear_filters():
    """ Clear any filters on the form when we re-load """
    db.Setting.query.filter_by(key='filter_game_session').delete()


def create_app():
    """ Set up the flask app and initialize global objects """
    # Create the flask application
    app = Flask(__name__)

    # set the configuration
    app.config.from_object(DevConfig())

    # initalize our globlal objects
    bs.init_app(app)
    db.init_app(app)

    from app.character.routes import character_bp
    app.register_blueprint(character_bp)

    from app.entry.routes import entry_bp
    app.register_blueprint(entry_bp)

    return app
