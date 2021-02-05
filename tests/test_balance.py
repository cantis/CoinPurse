""" Tests for transaction balances """
import pytest

from config import TestConfig
from web import db, create_app
from web.models import Entry, Setting, Character


@pytest.fixture(scope='session')
def app():
    app = create_app()
    config = TestConfig()
    app.config.from_object(config)
    return app


@pytest.fixture(scope='function')
def client(app):
    with app.app_context():
        # create the database
        client = app.test_client()
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
        db.session.add(Entry(id=5, game_session=1, description='Spear', amount=50.00, character_id=3))
        db.session.add(Entry(id=6, game_session=1, description='Backpack', amount=60.00, character_id=3))
        db.session.commit()

        yield client
        db.drop_all()


def test_balance_showing(client):
    # arrange

    # act
    rv = client.get('/entry', follow_redirects=True)

    # assert
    assert b'Balance:' in rv.data


def test_get_balance_character_one(client):
    # arrange

    # act
    rv = client.get('/entry', follow_redirects=True)

    # assert
    assert b'60.00' in rv.data


def test_get_balance_character_two(client):
    # arrange
    character_id = 3
    rv = client.post('/current_character', data=dict(selected_character=character_id), follow_redirects=True)

    # act
    rv = client.get('/entry', follow_redirects=True)

    # assert
    assert b'150.00' in rv.data
