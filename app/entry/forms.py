from wtforms.fields.core import FloatField, IntegerField
from wtforms.fields.simple import HiddenField, SubmitField
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired


# WTForms Definitions
class AddEntryForm(FlaskForm):
    """ Add Entry Form """
    game_session = IntegerField(label='Session', validators=[InputRequired('Please provide a game session number.')])
    description = StringField(label='Description', validators=[InputRequired('Please provide a name')])
    amount = FloatField(label='Amount', validators=[InputRequired('Please enter an amount.')])
    submit = SubmitField('Save')


class EditEntryForm(FlaskForm):
    """ Edit a transaction / entry Form """
    id = HiddenField()
    game_session = IntegerField(label='Session', validators=[InputRequired('Please provide game session number.')])
    description = StringField(label='Description', validators=[InputRequired('Please provide a name')])
    amount = FloatField(label='Amount', validators=[InputRequired('Please enter an amount.')])
    submit = SubmitField('Save')
