from flask import Flask, render_template, url_for, redirect, request
from wtforms.fields.core import BooleanField, FloatField, IntegerField
from wtforms.fields.simple import HiddenField
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy
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
#   >>>from app import db
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
    session = db.Column(db.Integer)
    description = db.Column(db.String(150), default='')
    amount = db.Column(db.Float)


class Character(db.Model):
    """ Represents a character """
    __tablename__ = 'Characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    is_dead = db.Column(db.Boolean, default=False)


class Setting(db.Model):
    """ Stores persistent settings for the application """
    __tablename__ = 'Settings'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(), nullable=False)
    value = db.Column(db.String(), nullable=False)


# Quick Forms
class AddEntryForm(FlaskForm):
    """ Add Entry Form """
    session = IntegerField(label='Session', validators=[InputRequired('Please provide session number.')])
    description = StringField(label='Description', validators=[InputRequired('Please provide a name')])
    amount = FloatField(label='Amount', validators=[InputRequired('Please enter an amount.')])


class EditEntryForm(FlaskForm):
    """ Edit a transaction / entry Form """
    id = HiddenField()
    session = IntegerField(label='Session', validators=[InputRequired('Please provide session number.')])
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


# Module Global
_current_character = Character()


# Route Handlers
@app.route('/', methods=['get'])
def index():
    entries = Entry.query.all()
    characters = Character.query.all()
    add_form = AddEntryForm()
    selected_name = ''
    if _current_character is not None:
        selected_name = _current_character.name
    # selected_name = 'Alpha'
    return render_template('index.html', entries=entries, add_form=add_form, characters=characters, selected_name=selected_name)


@app.route('/change_character', methods=['post'])
def change_character():
    selection = request.form.get('select_character')
    global _current_character
    _current_character = Character.query.get(selection)
    return redirect(url_for('index'))


@app.route('/add', methods=['post'])
def add_transaction():
    """ Handle adding a new transaction """
    form = AddEntryForm()
    if form.validate_on_submit():
        new_entry = Entry(
            id=form.id.data,
            session=form.session.data,
            description=form.description.data,
            amount=form.amount.data
            )
        db.session.add(new_entry)
        db.session.commit()

    return redirect(url_for('index'))


@app.route('/character', methods=['get'])
def character_list():
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


def set_current_character():
    """ Check the database for a previously set active character
    if one isn't set then set the 'first one in the database. """

    global _current_character

    # A filtered query
    # current = db.session.query(Setting).filter(Setting.key == 'current_character').all()

    # or another, shorter way
    # current = db.session.query(Setting).filter_by(key='current_character').all() 

    # Scalar value, single value if it exists or None
    # current = db.session.scalar(Setting).filter_by(key='current_character')
    current = Setting.scalar(Setting).filter_by(key='current_character')

    if not current:
        current = Character.first
        pass