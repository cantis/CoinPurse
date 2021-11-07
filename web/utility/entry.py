from flask import session

from web import db
from web.models import Entry, Character, Setting


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


def get_game_session_list(character_id, no_all=False):
    """ Return a distinct alpha list of all game sessions and a 'all' at top """
    # NOTE: Added an order by, note the \ for clean line continuation (this is up for debate)
    # SEE: https://stackoverflow.com/questions/22275412/sqlalchemy-return-all-distinct-column-values for Distinct keyword.

    games = db.session.query(Entry.game_session.distinct()) \
        .filter_by(character_id=character_id) \
        .order_by(Entry.game_session.asc()) \
        .all()

    # The distinct above returns a list of tupples, we need to convert that to a strait list
    # we use a lambda to map out the tupple indexes to a list

    game_sessions = list(map(lambda x: str(x[0]), games))

    if not no_all:
        # Add an 'ALL' at the top of the list.
        game_sessions.insert(0, 'All')

    return game_sessions
