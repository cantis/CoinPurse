from flask import Flask
from flask_bootstrap import Bootstrap
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from os import path

# create global objects
bs = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()


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

    from web.character.routes import character_bp
    app.register_blueprint(character_bp)

    from web.entry.routes import entry_bp
    app.register_blueprint(entry_bp)

    # if not path.exists('.\\web\\wallet.sqlite'):
    #     print('Path not Found: Call Create')
    #     db.create_all()
    # else:
    #     print('Path Found')

    return app
