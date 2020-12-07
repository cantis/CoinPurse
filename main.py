from flask import Flask, render_template, url_for, redirect, session
from flask.globals import request
from wtforms.fields.core import BooleanField, FloatField, IntegerField
from wtforms.fields.simple import HiddenField
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

app = Flask(__name__)


# Set Configuration
config = DevConfig()
app.config.from_object(config)


# Initialize DB object
db = SQLAlchemy(app)
# To create the database at the command line execute:
#   python
#   >>>from main import db (main the the file where the application is located)
#   >>>db.create_all()
#   >>>quit()
migrate = Migrate(app, db)
# see https://medium.com/@arnaud.bertrand/modifying-python-s-search-path-with-pth-files-2a41a4143574
# for information on adding a .pth path file to the virtual environment site-packages file that
# contains the path to the application root
# from the terminal ($)
# Iniatize migrations
#   $ flask db init
# Add a new migration
#   $ flask db migrate -m "migration name"
# Execute migration update
#   $ flask db upgrade

# Initalize Bootstrap
bs = Bootstrap()
bs.init_app(app)


# Models
class Entry(db.Model):
    """ Represents an entry in the purse """
    __tablename__ = 'Entries'
    id = db.Column(db.Integer, primary_key=True)
    game_session = db.Column(db.Integer)
    description = db.Column(db.String(150), default='')
    amount = db.Column(db.Float)
    character_id = Column(Integer, ForeignKey('Characters.id'))


class Character(db.Model):
    """ Represents a character """
    __tablename__ = 'Characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    is_dead = db.Column(db.Boolean, default=False)
    entries = relationship('Entry', backref='character')


class Setting(db.Model):
    """ Stores persistent settings for the application """
    __tablename__ = 'Settings'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(), nullable=False)
    value = db.Column(db.String(), nullable=False)


# Quick Forms
class AddEntryForm(FlaskForm):
    """ Add Entry Form """
    game_session = IntegerField(label='Session', validators=[InputRequired('Please provide a game session number.')])
    description = StringField(label='Description', validators=[InputRequired('Please provide a name')])
    amount = FloatField(label='Amount', validators=[InputRequired('Please enter an amount.')])


class EditEntryForm(FlaskForm):
    """ Edit a transaction / entry Form """
    id = HiddenField()
    game_session = IntegerField(label='Session', validators=[InputRequired('Please provide game session number.')])
    description = StringField(label='Description', validators=[InputRequired('Please provide a name')])
    amount = FloatField(label='Amount', validators=[InputRequired('Please enter an amount.')])


class AddCharacterForm(FlaskForm):
    """ Add Character Form """
    name = StringField(label="Character", validators=[InputRequired('Please provide a character name')])
    is_dead = BooleanField(label="Is Dead")


class EditCharacterForm(FlaskForm):
    """ Edit Character Form """
    id = HiddenField()
    name = StringField(label="Character", validators=[InputRequired('Please provide a character name')])
    is_dead = BooleanField(label="Is Dead")


# Route Handlers
@app.route('/', methods=['get'])
def index():
    current_id = get_current_character_id()
    if current_id is None:
        return redirect(url_for('character_list'))

    selected_name = Character.query.filter_by(id=current_id).first().name
    entries = Entry.query.filter_by(character_id=current_id)
    characters = Character.query.all()
    add_form = AddEntryForm()
    if 'game_session' in session:
        add_form.game_session.data = session['game_session']
    return render_template('index.html', entries=entries, add_form=add_form, characters=characters, selected_name=selected_name)


@app.route('/add', methods=['post'])
def add_transaction():
    """ Handle adding a new transaction """
    form = AddEntryForm()
    if form.validate_on_submit():
        new_entry = Entry(
            game_session=form.game_session.data,
            description=form.description.data,
            amount=form.amount.data,
            character_id=get_current_character_id()
            )
        db.session.add(new_entry)
        db.session.commit()

        # Save the session for re-use
        session['game_session'] = form.game_session.data

    return redirect(url_for('index'))


@app.route('/character', methods=['get'])
def character_list():
    """ show character list """
    characters = Character.query.all()
    form = AddCharacterForm()
    form.process(obj=characters)
    form.name(class_='col-md-4')
    return render_template('character.html', characters=characters, form=form, mode='add')


@app.route('/character/<id>', methods=['get', 'post'])
def edit_character(id):
    """ Handle editing an existing Character """
    # The single character we are editing
    character = Character.query.get(id)
    # Data for the list of characters
    characters = Character.query.all()

    form = EditCharacterForm()
    mode = ''

    if form.validate_on_submit():
        character.id = int(form.id.data)
        character.name = form.name.data
        character.is_dead = form.is_dead.data
        db.session.commit()
        form = AddCharacterForm()
        character = None
        mode = 'add'
    else:
        mode = 'edit'

    form.process(obj=characters)
    form.process(obj=character)
    return render_template('character.html', characters=characters, character=character, form=form, mode=mode)


@app.route('/character/add', methods=['post'])
def add_character():
    """ Handle adding a new Character """
    form = AddCharacterForm()
    if form.validate_on_submit():
        new_character = Character(
            name=form.name.data,
            is_dead=form.is_dead.data
            )
        db.session.add(new_character)
        db.session.commit()

    return redirect(url_for('character_list'))


@app.route('/current_character', methods=['post'])
def set_current_character():
    """ handle setting the current character """
    id = request.form['selected_character']
    char = Character.query.get(id)
    if char is not None:
        setting = Setting.query.filter_by(key='current_character').first()
        if setting is not None:
            setting.value = str(char.id)
            db.session.commit()
        else:
            db.session.add(Setting(key='current_character', value=str(char.id)))
            db.session.commit()
        session['current_character'] = char.id
        return redirect(url_for('index'))


def get_current_character_id():
    """ Check the database for a previously set active character
    if one isn't set then set the 'first one in the database. """

    # A filtered query
    # current = db.session.query(Setting).filter(Setting.key == 'current_character').all()

    # or another, shorter way
    # current = db.session.query(Setting).filter_by(key='current_character').all()

    # Scalar value, single value if it exists or None
    # current = db.session.scalar(Setting).filter_by(key='current_character')
    # current = Setting.scalar(Setting).filter_by(key='current_character')

    # see if their is a character id in session
    if 'current_character' in session:
        return session['current_character']

    # See if there is a saved character id on the database, if so set it to current
    current_id = Setting.query.filter_by(key='current_character').first()
    char = Character()

    if current_id is None:
        # no current_id has been saved try and get the first Character on the Character table and use that.
        char = Character.query.first()
        if char is None:
            return None

    else:
        # Ok we have a character on the database, pull it up
        char = Character.query.filter_by(id=current_id.value).first()
        # now we can save the right data
        db.session.add(Setting(key='current_character', value=str(char.id)))
        db.session.commit

    # set the character we found up in session
    session['current_character'] = char.id
    return char.id
