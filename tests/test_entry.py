""" Tests involved in CRUD for transaction Entries """
import pytest

from config import TestConfig
from main import app, db, Entry, Character, Setting


@pytest.fixture
def client(scope='function'):
    config = TestConfig()
    app.config.from_object(config)

    with app.test_client() as client:
        # Create the Database
        with app.app_context():
            db.create_all()
        # Add some Characters
        db.session.add(Character(id=1, name='Paladin', is_dead=False))
        db.session.add(Character(id=2, name='Rogue', is_dead=False))
        db.session.add(Character(id=3, name='Fighter', is_dead=False))
        db.session.commit()

        # Set the current Character
        db.session.add(Setting(key='current_character', value='2'))
        db.session.commit()

        yield client
        db.drop_all()


@pytest.fixture
def entry_client(scope='function'):
    config = TestConfig()
    app.config.from_object(config)
    with app.test_client() as entry_client:
        # create the database

        with app.app_context():
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
        db.session.add(Entry(id=3, game_session=1, description='Potion', amount=30.00, character_id=2))
        db.session.add(Entry(id=4, game_session=1, description='Crossbow', amount=40.00, character_id=3))
        db.session.add(Entry(id=5, game_session=1, description='Spear', amount=50.00, character_id=4))
        db.session.add(Entry(id=6, game_session=1, description='Backpack', amount=60.00, character_id=5))
        db.session.commit()

        yield entry_client
        db.drop_all()


def test_create_entry(client):
    # arrange

    # act
    rv = client.post('/add', data=dict(game_session=1, description='Wand of Heal', amount=10.02), follow_redirects=True)

    # assert
    assert b'Wand of Heal' in rv.data
    result = Entry.query.filter_by(description='Wand of Heal').first()
    assert result is not None


def test_create_entry_check_game_session(client):
    # arrange

    # act
    client.post('/add', data=dict(game_session=1, description='Wand of Heal', amount=10.02), follow_redirects=True)

    # assert
    result = Entry.query.filter_by(description='Wand of Heal').first()
    assert result.game_session == 1


def test_create_entry_check_description(client):
    # arrange

    # act
    client.post('/add', data=dict(game_session=1, description='Wand of Heal', amount=10.02), follow_redirects=True)

    # assert
    result = Entry.query.filter_by(description='Wand of Heal').first()
    assert result.description == 'Wand of Heal'


def test_create_entry_check_amount(client):
    # arrange

    # act
    client.post('/add', data=dict(game_session=1, description='Wand of Heal', amount=10.02), follow_redirects=True)

    # assert
    result = Entry.query.filter_by(description='Wand of Heal').first()
    assert result.amount == 10.02


def test_create_entry_check_displayed_game_session(client):
    # arrange

    # act
    rv = client.post('/add', data=dict(game_session=567, description='Wand of Heal', amount=45.89), follow_redirects=True)

    # assert
    assert b'567' in rv.data


def test_create_entry_check_displayed_description(client):
    # arrange

    # act
    rv = client.post('/add', data=dict(game_session=567, description='Wand of Heal', amount=45.89), follow_redirects=True)

    # assert
    assert b'Wand of Heal' in rv.data


def test_create_entry_check_displayed_amount(client):
    # arrange

    # act
    rv = client.post('/add', data=dict(game_session=567, description='Wand of Heal', amount=45.89), follow_redirects=True)

    # assert
    assert b'45.89' in rv.data


def test_entries_change_for_character(entry_client):

    entry_client.post('/current_character', data=dict(selected_character=2), follow_redirects=True)
    rv1 = entry_client.get('/', follow_redirects=True)
    assert b'Wand' in rv1.data

    entry_client.post('/current_character', data=dict(selected_character=3), follow_redirects=True)
    rv2 = entry_client.get('/', follow_redirects=True)
    assert b'Spear' in rv2.data
