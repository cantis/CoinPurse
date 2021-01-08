from flask import Blueprint, render_template, redirect, url_for, session, request
from app.entry.forms import AddEntryForm, EditEntryForm
from app.entry.models import Entry, Setting
from app.character.models import Character
from app import db
from app.entry.utility import get_current_character_id, get_balance

entry_bp = Blueprint('entry_bp', __name__, template_folder='templates')


@entry_bp.route('/', methods=['GET'])
@entry_bp.route('/entry', methods=['GET'])
def index():
    current_id = get_current_character_id()
    if current_id is None:
        return redirect(url_for('character_bp.character_list'))

    selected_name = Character.query.filter_by(id=current_id).first().name
    entries = Entry.query.filter_by(character_id=current_id)
    characters = Character.query.all()
    form = AddEntryForm()
    balance = get_balance()
    mode = 'add'
    if 'game_session' in session:
        form.game_session.data = session['game_session']
    return render_template('index.html', mode=mode, entries=entries, form=form,
                           characters=characters, selected_name=selected_name, balance=balance)


@entry_bp.route('/entry/add', methods=['post'])
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

    return redirect(url_for('entry_bp.index'))


@entry_bp.route('/entry/<id>', methods=['get', 'post'])
def edit_entry(id):
    """ Handle editing an existing entry """
    entry = Entry.query.get(id)
    entries = Entry.query.all()
    current_id = get_current_character_id()
    selected_name = Character.query.filter_by(id=current_id).first().name
    characters = Character.query.all()
    balance = get_balance()

    form = EditEntryForm()
    mode = ''

    if form.validate_on_submit():
        entry.id = int(form.id.data)
        entry.game_session = form.game_session.data
        entry.description = form.description.data
        entry.amount = float(form.amount.data)
        db.session.commit()
        form = AddEntryForm()
        entry = None
        mode = 'add'
    else:
        mode = 'edit'

    form.process(obj=entries)
    form.process(obj=entry)
    return render_template('index.html', form=form, mode=mode, entry=entry,
                           entries=entries, characters=characters, selected_name=selected_name, balance=balance)


@entry_bp.route('/current_character', methods=['post'])
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
        return redirect(url_for('entry_bp.index'))