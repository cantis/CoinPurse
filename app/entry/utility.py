from app.entry.models import Entry
from app.setting.models import Setting
from app.character.models import Character
from app import db
from flask import session


def get_balance():
    """ Get the balance for a character """
    character_id = get_current_character_id()
    entries = Entry.query.filter_by(character_id=character_id)
    balance = 0
    for entry in entries:
        balance += entry.amount
    return balance


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
