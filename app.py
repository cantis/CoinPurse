from flask import Flask, render_template, url_for, redirect
from wtforms.fields.core import BooleanField, FloatField, IntegerField
from wtforms.fields.simple import HiddenField
from config import DevConfig
from flask_table import Table, Col
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


# HTML Tables
class EntriesTable(Table):
    """ Defines an flask_table for Entries """
    classes = ['table']
    table_id = 'tranTable'
    thead_classes = ['table__header']
    no_items = 'No Transactions Recorded'

    def get_tr_attrs(self, item):
        return{'class': 'table__row'}
    id = Col('Id', th_html_attrs={'class': 'table__header'}, td_html_attrs={'class': 'table__cell'})
    session = Col('Session', th_html_attrs={'class': 'table__header'}, td_html_attrs={'class': 'table__cell'})
    description = Col('Description', th_html_attrs={'class': 'table__header'}, td_html_attrs={'class': 'table__cell'})
    amount = Col('Amount', th_html_attrs={'class': 'table__header'}, td_html_attrs={'class': 'table__cell'})


class CharacterTable(Table):
    """ Defines a flask_table listing Characters """
    classes = ['table']
    table_id = 'characterTable'
    thead_classes = ['table__header']
    no_items = 'No Character Defined'

    def get_tr_attrs(self, item):
        return{'class': 'table__row'}
    name = Col('Character', th_html_attrs={'class': 'table__header'}, td_html_attrs={'class': 'table__cell'})
    is_dead = Col('Is Dead', th_html_attrs={'class': 'table__header'}, td_html_attrs={'class': 'table__cell'})


# Quick Forms
class AddEntryForm(FlaskForm):
    """ Add Entry Form """
    session = IntegerField(label='Session', validators=[InputRequired('Please provide session number.')])
    description = StringField(label='Description', validators=[InputRequired('Please provide a name')])
    amount = FloatField(label='Amount', validators=[InputRequired('Please enter an amount.')])


class EditEntryForm(FlaskForm):
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


# Route Handlers
@app.route('/', methods=['get'])
def index():
    entries = Entry.query.all()
    add_form = AddEntryForm()
    return render_template('index.html', entries=entries, add_form=add_form)


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
    character_table = CharacterTable(characters)
    add_character_form = AddCharacterForm()
    return render_template('character.html', character_table=character_table, add_character_form=add_character_form)


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
