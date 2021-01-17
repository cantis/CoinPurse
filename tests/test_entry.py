""" Tests involved in CRUD for transaction Entries """
import pytest
from app import create_app, db
from config import TestConfig
from app.entry.models import Entry
from app.setting.models import Setting
from app.character.models import Character


@pytest.fixture(scope='session')
def app():
    app = create_app()
    config = TestConfig()
    app.config.from_object(config)
    return app


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


def test_create_entry(client):
    # arrange

    # act
    rv = client.post('/entry/add', data=dict(game_session=1, description='Wand of Heal', amount=10.02), follow_redirects=True)

    # assert
    assert b'Wand of Heal' in rv.data
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
    rv = Entry.query.filter_by(description='Wand of Heal').first()
    assert rv.amount == 10.02


def test_edit_entry_description(entry_client):
    # arrange

    # act
    data = dict(id=2, game_session=1, description='Flail', amount=20.00)
    rv = entry_client.post('/entry/2', data=data, follow_redirects=True)

    # assert
    entry = Entry.query.get(2)
    assert entry.game_session == 1
    assert entry.description == 'Flail'
    assert entry.amount == 20.00
    assert b'Add Entry' in rv.data


def test_edit_entry_session(entry_client):
    # arrange

    # act
    data = dict(id=2, game_session=5, description='Sword', amount=20.00)
    rv = entry_client.post('/entry/2', data=data, follow_redirects=True)

    # assert
    entry = Entry.query.get(2)
    assert entry.game_session == 5
    assert entry.description == 'Sword'
    assert entry.amount == 20.00
    assert b'Add Entry' in rv.data


def test_edit_entry_amount(entry_client):
    # arrange

    # act
    data = dict(id=2, game_session=1, description='Sword', amount=24.00)
    rv = entry_client.post('/entry/2', data=data, follow_redirects=True)

    # assert
    entry = Entry.query.get(2)
    assert entry.game_session == 1
    assert entry.description == 'Sword'
    assert entry.amount == 24.00
    assert b'Add Entry' in rv.data


def test_edit_entry(client):
    # arrange

    # act
    rv = client.post('/entry/2')

    # assert
    assert b'Edit' in rv.data


def test_default_path(client):
    # arrange

    # act
    rv = client.get('/')

    # assert
    assert b'Add Entry' in rv.data


def test_entry_path(client):
    # arrange

    # act
    rv = client.get('/entry')

    # assert
    assert b'Add Entry' in rv.data


def test_create_entry_check_displayed_game_session(client):
    # arrange

    # act
    rv = client.post('/entry/add', data=dict(game_session=567, description='Wand of Heal', amount=45.89), follow_redirects=True)

    # assert
    assert b'567' in rv.data


def test_create_entry_check_displayed_description(client):
    # arrange

    # act
    rv = client.post('/entry/add', data=dict(game_session=567, description='Wand of Heal', amount=45.89), follow_redirects=True)

    # assert
    assert b'Wand of Heal' in rv.data


def test_create_entry_check_displayed_amount(client):
    # arrange

    # act
    rv = client.post('/entry/add', data=dict(game_session=567, description='Wand of Heal', amount=45.89), follow_redirects=True)

    # assert
    assert b'45.89' in rv.data


def test_entries_change_by_character(entry_client):
    # a two stage test, do it once, change character and check again, the
    # entries displayed should switch each time.

    # arrange
    entry_client.post('/current_character', data=dict(selected_character=2), follow_redirects=True)
    # act
    rv1 = entry_client.get('/entry', follow_redirects=True)
    # assert
    assert b'Sword' in rv1.data
    assert b'Spear' not in rv1.data

    # arrange
    entry_client.post('/current_character', data=dict(selected_character=3), follow_redirects=True)
    # act
    rv2 = entry_client.get('/entry', follow_redirects=True)
    # assert
    assert b'Spear' in rv2.data
    assert b'Sword' not in rv2.data
