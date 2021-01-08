from flask import Blueprint, render_template, redirect, url_for
from app.character.forms import AddCharacterForm, EditCharacterForm
from app.character.models import Character
from app import db

character_bp = Blueprint('character_bp', __name__, template_folder='templates')


@character_bp.route('/character', methods=['get'])
def character_list():
    """ charactersshow character list """
    characters = Character.query.all()
    form = AddCharacterForm()
    form.process(obj=characters)
    form.name(class_='col-md-4')
    return render_template('character.html', characters=characters, form=form, mode='add')


@character_bp.route('/character/<id>', methods=['get', 'post'])
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


@character_bp.route('/character/add', methods=['post'])
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

    return redirect(url_for('character_bp.character_list'))
