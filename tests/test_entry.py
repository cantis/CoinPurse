""" Tests involved in CRUD for transaction Entries """
import pytest
from werkzeug.security import generate_password_hash

from web import create_app, db
from web.models import Entry, Setting, Character, User
from config import TestConfig


@pytest.fixture(scope='session')
def app():
    app = create_app()
    config = TestConfig()
    app.config.from_object(config)
    return app


@pytest.fixture(scope='function')
def empty_client(app):
    with app.app_context():
        empty_client = app.test_client()
        db.create_all()

        password = generate_password_hash('Monday1')
        db.session.add(User(id=1, first_name='Test', last_name='User', email='someone@noplace.com', password=password))
        db.session.commit()

        data = dict(email='someone@noplace.com', password='Monday1', remember_me=False)
        empty_client.post('/login', data=data)

        yield empty_client
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
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
        db.session.add(Entry(id=5, game_session=1, description='Spear', amount=50.00, character_id=3))
        db.session.add(Entry(id=6, game_session=2, description='Backpack', amount=60.00, character_id=3))
        db.session.commit()

        yield entry_client
        db.drop_all()


def test_handle_character_no_entries(empty_client):
    """ confirm the application can start up correctly without any characters or entries in the db """
    # arrange

    # Add some Characters
    db.session.add(Character(id=1, name='Paladin', is_dead=False))
    db.session.add(Character(id=2, name='Rogue', is_dead=False))
    db.session.add(Character(id=3, name='Fighter', is_dead=False))
    db.session.commit()

    # Set the current Character
    db.session.add(Setting(key='current_character', value='2'))
    db.session.commit()

    # act
    result = empty_client.get('/', follow_redirects=True)

    # assert
    assert b'Entries' in result.data


def test_handle_no_character_no_entries(empty_client):
    """ confirm the application can start up correctly without any characters or entries in the db """
    # arrange

    # act
    result = empty_client.get('/', follow_redirects=True)

    # assert
    assert b'Characters' in result.data


def test_create_entry(client):
    # arrange

    # act
    result = client.post('/entry/add', data=dict(game_session=1, description='Wand of Heal', amount=10.02), follow_redirects=True)

    # assert
    assert b'Wand of Heal' in result.data
    result = Entry.query.filter_by(description='Wand of Heal').first()
    assert result is not None


def test_create_entry_check_game_session(client):
    # arrange

    # act
    client.post('/entry/add', data=dict(game_session=1, description='Wand of Heal', amount=10.02), follow_redirects=True)

    # assert
    result = Entry.query.filter_by(description='Wand of Heal').first()
    assert result.game_session == 1


def test_create_entry_check_description(client):
    # arrange

    # act
    client.post('/entry/add', data=dict(game_session=1, description='Wand of Heal', amount=10.02), follow_redirects=True)

    # assert
    result = Entry.query.filter_by(description='Wand of Heal').first()
    assert result.description == 'Wand of Heal'


def test_create_entry_check_amount(client):
    # arrange

    # act
    client.post('/entry/add', data=dict(game_session=1, description='Wand of Heal', amount=10.02), follow_redirects=True)

    # assert
    result = Entry.query.filter_by(description='Wand of Heal').first()
    assert result.amount == 10.02


def test_edit_entry_description(entry_client):
    # arrange

    # act
    data = dict(id=2, game_session=1, description='Flail', amount=20.00)
    result = entry_client.post('/entry/2', data=data, follow_redirects=True)

    # assert
    entry = Entry.query.get(2)
    assert entry.game_session == 1
    assert entry.description == 'Flail'
    assert entry.amount == 20.00
    assert b'Add Entry' in result.data


def test_edit_entry_session(entry_client):
    # arrange

    # act
    data = dict(id=2, game_session=5, description='Sword', amount=20.00)
    result = entry_client.post('/entry/2', data=data, follow_redirects=True)

    # assert
    entry = Entry.query.get(2)
    assert entry.game_session == 5
    assert entry.description == 'Sword'
    assert entry.amount == 20.00
    assert b'Add Entry' in result.data


def test_edit_entry_amount(entry_client):
    # arrange

    # act
    data = dict(id=2, game_session=1, description='Sword', amount=24.00)
    result = entry_client.post('/entry/2', data=data, follow_redirects=True)

    # assert
    entry = Entry.query.get(2)
    assert entry.game_session == 1
    assert entry.description == 'Sword'
    assert entry.amount == 24.00
    assert b'Add Entry' in result.data


def test_edit_entry(client):
    # arrange

    # act
    result = client.post('/entry/2')

    # assert
    assert b'Edit' in result.data


def test_default_path(client):
    # arrange

    # act
    result = client.get('/')

    # assert
    assert b'Add Entry' in result.data


def test_entry_path(client):
    # arrange

    # act
    result = client.get('/entry')

    # assert
    assert b'Add Entry' in result.data


def test_create_entry_check_displayed_game_session(client):
    # arrange

    # act
    result = client.post('/entry/add', data=dict(game_session=567, description='Wand of Heal', amount=45.89), follow_redirects=True)

    # assert
    assert b'567' in result.data


def test_create_entry_check_displayed_description(client):
    # arrange

    # act
    result = client.post('/entry/add', data=dict(game_session=567, description='Wand of Heal', amount=45.89), follow_redirects=True)

    # assert
    assert b'Wand of Heal' in result.data


def test_create_entry_check_displayed_amount(client):
    # arrange

    # act
    result = client.post('/entry/add', data=dict(game_session=567, description='Wand of Heal', amount=45.89), follow_redirects=True)

    # assert
    assert b'45.89' in result.data


def test_entries_change_by_character(entry_client):
    # a two stage test, do it once, change character and check again, the
    # entries displayed should switch each time.

    # arrange
    with entry_client.application.test_request_context('/'):
        entry_client.post('/current_character', data=dict(selected_character=2), follow_redirects=True)
        # act
        result1 = entry_client.get('/entry', follow_redirects=True)
        # assert
        assert b'Sword' in result1.data
        assert b'Spear' not in result1.data

        # arrange
        entry_client.post('/current_character', data=dict(selected_character=3), follow_redirects=True)
        # act
        result2 = entry_client.get('/entry', follow_redirects=True)
        # assert
        assert b'Sword' not in result2.data
        assert b'Spear' in result2.data
