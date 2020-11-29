""" Tests for setting the currently selected character """

import pytest

from main import app, db, Character
from config import TestConfig


@pytest.fixture
def client(scope='function'):
    config = TestConfig()
    app.config.from_object(config)

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        db.session.add(Character(id=1, name='Paladin', is_dead=False))
        db.session.add(Character(id=2, name='Rogue', is_dead=False))
        db.session.add(Character(id=3, name='Fighter', is_dead=False))
        db.session.commit()
        yield client
        db.drop_all()


def test_set_current_character(client):
    # arrange
    character_id = 2

    # act
    rv = client.post('/change_character', data=dict(select_character=character_id), follow_redirects=True)

    # assert
    assert b'Rogue' in rv.data


def test_current_character_none(client):
    """ Get the current character, with none set and none created """
    # arrange

    # act
    rv = client.get('/')

    # assert
    assert b'Paladin' in rv.data