from flask_wtf import FlaskForm
from wtforms.fields.core import BooleanField
from wtforms.fields.simple import HiddenField
from wtforms import StringField
from wtforms.validators import InputRequired


class AddCharacterForm(FlaskForm):
    """ Add Character Form """
    name = StringField(label="Character", validators=[InputRequired('Please provide a character name')])
    is_dead = BooleanField(label="Is Dead")


class EditCharacterForm(FlaskForm):
    """ Edit Character Form """
    id = HiddenField()
    name = StringField(label="Character", validators=[InputRequired('Please provide a character name')])
    is_dead = BooleanField(label="Is Dead")
