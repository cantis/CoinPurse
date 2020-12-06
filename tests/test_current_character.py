""" Tests for setting the currently selected character """

import pytest

from main import app, db, Character, Setting
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
    rv = client.post('/current_character', data=dict(selected_character=character_id), follow_redirects=True)

    # assert
    assert rv.status_code == 200


def test_current_character_no_db_no_records():
    # arrange
    config = TestConfig()
    app.config.from_object(config)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()

    # act
    rv = client.get('/')

    # assert
    assert b'Paladin' not in rv.data


def test_current_character_not_set(client):
    """ Get the current character, with none set """
    # arrange

    # act
    rv = client.get('/')

    # assert
    assert b'Paladin' in rv.data


def test_saved_character_setting(client):
    """ get_current_character from Settings table """
    # arrange
    character_id = 3
    client.post('/current_character', data=dict(selected_character=character_id), follow_redirects=True)

    # act
    rv = client.get('/')

    # assert
    assert b'Fighter' in rv.data


def test_check_setting_saved(client):
    """ Chehck that the setting is saved to the table when it's changed """
    # arrange
    # character_id = 2
    # client.post('/current_character', data=dict(id=character_id), follow_redirects=True)
    db.session.add(Setting(key='current_character', value='2'))
    db.session.commit()

    # act
    character_id = 3
    client.post('/current_character', data=dict(selected_character=character_id), follow_redirects=True)

    # assert
    current_character = Setting.query.filter_by(key='current_character').first()
    assert current_character.value == '3'


def test_get_current_character_id(client):
    # arrange
    db.session.add(Setting(key='current_character', value='2'))
    db.session.commit()

    # act
    rv = rv = client.get('/')

    # assert
    assert b'Rogue' in rv.data
