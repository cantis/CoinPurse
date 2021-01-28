from flask import Blueprint, render_template, redirect, url_for, request

from app import db
from app.entry.forms import AddEntryForm, EditEntryForm
from app.entry.models import Entry
from app.entry.utility import get_current_character_id, get_balance, get_game_session_list
from app.character.models import Character
from app.setting.utility import get_setting, save_setting

entry_bp = Blueprint('entry_bp', __name__, template_folder='templates')


@entry_bp.route('/', methods=['GET'])
@entry_bp.route('/entry', methods=['GET'])
def index():
    current_id = get_current_character_id()
    if current_id is None:
        return redirect(url_for('character_bp.character_list'))

    selected_name = Character.query.filter_by(id=current_id).first().name
    characters = Character.query.all()
    game_session_list = get_game_session_list(current_id)
    filter_game_session = get_setting('filter_game_session', 'All')

    if filter_game_session == 'All':
        entries = Entry.query.filter_by(character_id=current_id)
    else:
        entries = Entry.query.filter_by(character_id=current_id, game_session=filter_game_session)

    form = AddEntryForm()
    balance = get_balance()
    mode = 'add'
    game_session = get_setting('game_session')

    return render_template('index.html', mode=mode, entries=entries, form=form, game_session=game_session,
                           characters=characters, selected_name=selected_name, balance=balance,
                           game_session_list=game_session_list, filter_game_session=filter_game_session)


@entry_bp.route('/filter_game_session', methods=['post'])
def game_session():
    """ set game_session for entries """
    sess = request.form['filter_game_session']
    save_setting('filter_game_session', sess)
    return redirect(url_for('entry_bp.index'))


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
        save_setting('game_session', form.game_session.data)

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
    game_session_list = get_game_session_list(current_id)
    selected_game_session = get_setting('filter_game_session', 'All')

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
                           entries=entries, characters=characters, selected_name=selected_name, balance=balance,
                           game_session_list=game_session_list, selected_game_session=selected_game_session)


@entry_bp.route('/current_character', methods=['post'])
def set_current_character():
    """ handle setting the current character """

    # new id from the form
    id = request.form['selected_character']

    # try and pull it from the db (we should be able to)
    char = Character.query.get(id)

    if char is not None:
        save_setting('current_character', str(char.id))
        save_setting('selected_game_session', 'All')

    return redirect(url_for('entry_bp.index'))
