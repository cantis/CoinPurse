""" Tests involved in CRUD for transaction Entries """
import pytest
from web import create_app, db
from config import TestConfig
from web.entry.models import Entry
from web.entry.utility import get_game_session_list
from web.setting.models import Setting
from web.character.models import Character


@pytest.fixture(scope='session')
def app():
    """ Application Fixture """
    app = create_app()
    config = TestConfig()
    app.config.from_object(config)
    return app


@pytest.fixture(scope='function')
def client(app):
    """ Fixture with basic data in it """

    with app.app_context():
        client = app.test_client()
        db.create_all()

        # Add some Characters db.session.add(Character(id=1, name='Paladin', is_dead=False))
        db.session.add(Character(id=2, name='Rogue', is_dead=False))
        db.session.add(Character(id=3, name='Fighter', is_dead=False))
        db.session.commit()

        # Set the current Character
        db.session.add(Setting(key='current_character', value='2'))
        db.session.commit()

        yield client
        db.drop_all()


@pytest.fixture(scope='function')
def entry_client(app):
    """ Fixture with more test data in it """

    with app.app_context():
        entry_client = app.test_client()
        db.create_all()

        # Add some Characters
        db.session.add(Character(id=1, name='Paladin', is_dead=False))
        db.session.add(Character(id=2, name='Rogue', is_dead=False))
        db.session.add(Character(id=3, name='Fighter', is_dead=False))
        db.session.commit()

        # Set the current Character
        db.session.add(Setting(key='current_character', value='2'))
        db.session.commit()

        # Add some entries
        db.session.add(Entry(id=1, game_session=1, description='Wand', amount=10.00, character_id=2))
        db.session.add(Entry(id=2, game_session=1, description='Sword', amount=20.00, character_id=2))
        db.session.add(Entry(id=3, game_session=2, description='Potion', amount=30.00, character_id=2))
        db.session.add(Entry(id=4, game_session=1, description='Crossbow', amount=40.00, character_id=3))
        db.session.add(Entry(id=5, game_session=2, description='Spear', amount=50.00, character_id=3))
        db.session.add(Entry(id=6, game_session=3, description='Backpack', amount=60.00, character_id=3))
        db.session.commit()

        yield entry_client
        db.drop_all()


def test_character_game_sessions(entry_client):
    # arrange
    test_character = 3

    # act
    result = get_game_session_list(test_character, True)

    # assert
    assert len(result) == 3
    assert result[0] == '1'
    assert result[1] == '2'
    assert result[2] == '3'


def test_character_game_value_not_in(entry_client):
    """ Confirm we are getting just the values for a given character and not other data """

    # arrange
    test_character = 2

    # act
    result = get_game_session_list(test_character, True)

    # assert
    assert len(result) == 2
    assert '3' not in result


def test_confirm_all_added(entry_client):
    """ Confirm that the 'all' has been added to the beginning of the list """

    # arrange
    test_character = 3

    # act
    result = get_game_session_list(test_character)

    # assert
    assert len(result) == 4
    assert result[0] == 'All'
