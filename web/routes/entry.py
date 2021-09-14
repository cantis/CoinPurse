from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.core import FloatField, IntegerField
from wtforms.fields.simple import HiddenField, SubmitField
from wtforms.validators import InputRequired

from web import db
from web.models import Entry, Character
from web.utility.entry import get_current_character_id, get_balance, get_game_session_list
from web.utility.setting import get_setting, save_setting

entry_bp = Blueprint('entry_bp', __name__, template_folder='templates')


@entry_bp.route('/', methods=['GET'])
@entry_bp.route('/entry', methods=['GET'])
@login_required
def index():
    current_id = get_current_character_id()
    if current_id is None:
        return redirect(url_for('character_bp.character_list'))

    selected_character = Character.query.filter_by(id=current_id).first()
    if selected_character:
        selected_name = selected_character.name
    else:
        selected_name = ''
    characters = Character.query.filter_by(user_id=current_user.id).all()
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
                           game_session_list=game_session_list, filter_game_session=filter_game_session,
                           current_user=current_user)


@entry_bp.route('/filter_game_session', methods=['post'])
@login_required
def game_session():
    """ set game_session for entries """
    sess = request.form['filter_game_session']
    save_setting('filter_game_session', sess)
    return redirect(url_for('entry_bp.index'))


@entry_bp.route('/entry/add', methods=['post'])
@login_required
def add_transaction():
    """ Handle adding a new transaction """
    form = AddEntryForm()
    if form.validate_on_submit():

        user = current_user

        # get the value of the transaction, set to negative for withdrawl (i.e. purchase)
        entry_type = request.form['entry_type']
        if entry_type == 'withdrawl':
            amount = -form.amount.data
        if entry_type == 'deposit':
            amount = form.amount.data

        new_entry = Entry(
            game_session=form.game_session.data,
            description=form.description.data,
            amount=amount,
            character_id=get_current_character_id()
            )
        db.session.add(new_entry)
        try:
            db.session.commit()
        except Exception as ex:
            print(ex)

        # Save the session for re-use
        save_setting('game_session', form.game_session.data)

    return redirect(url_for('entry_bp.index'))


@entry_bp.route('/entry/<int:id>', methods=['get', 'post'])
@login_required
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
        amount = float(form.amount.data)

        entry_type = request.form['entry_type']
        if entry_type == 'withdrawl':
            amount = -amount
        entry.amount = amount

        db.session.commit()
        form = AddEntryForm()
        entry = None
        mode = 'add'
    else:
        if entry.amount < 0:
            entry_type = 'withdrawl'
        else:
            entry_type = 'deposit'
        mode = 'edit'

    form.process(obj=entries)
    form.process(obj=entry)
    return render_template('index.html', form=form, mode=mode, entry=entry,
                           entries=entries, characters=characters, selected_name=selected_name, balance=balance,
                           game_session_list=game_session_list, selected_game_session=selected_game_session, entry_type=entry_type)


@entry_bp.route('/current_character', methods=['post'])
@login_required
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
