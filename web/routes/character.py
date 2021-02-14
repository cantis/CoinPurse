from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms.fields.core import BooleanField, IntegerField
from wtforms.fields.simple import HiddenField
from wtforms import StringField
from wtforms.validators import InputRequired

from web import db
from web.models import Character

character_bp = Blueprint('character_bp', __name__, template_folder='templates')


@character_bp.route('/character', methods=['get'])
@login_required
def character_list():
    """ charactersshow character list """
    characters = Character.query.all()
    characters = Character.query.filter_by(user_id=current_user.id)
    form = AddCharacterForm()
    form.process(obj=characters)
    form.name(class_='col-md-4')
    return render_template('character.html', characters=characters, form=form, mode='add', current_user=current_user)


@character_bp.route('/character/<id>', methods=['get', 'post'])
@login_required
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
    return render_template('character.html', characters=characters, character=character, form=form, mode=mode, current_user=current_user)


@character_bp.route('/character/add', methods=['post'])
@login_required
def add_character():
    """ Handle adding a new Character """
    form = AddCharacterForm()
    if form.validate_on_submit():
        new_character = Character(
            name=form.name.data,
            is_dead=form.is_dead.data,
            user_id=current_user.id
            )
        db.session.add(new_character)
        db.session.commit()

    return redirect(url_for('character_bp.character_list'))


class AddCharacterForm(FlaskForm):
    """ Add Character Form """
    name = StringField(label="Character", validators=[InputRequired('Please provide a character name')])
    is_dead = BooleanField(label="Is Dead")


class EditCharacterForm(FlaskForm):
    """ Edit Character Form """
    id = HiddenField()
    name = StringField(label="Character", validators=[InputRequired('Please provide a character name')])
    is_dead = BooleanField(label="Is Dead")