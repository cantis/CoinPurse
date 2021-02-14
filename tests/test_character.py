""" Tests related to CRUD operations for Characters """
import pytest
from werkzeug.security import generate_password_hash

from web import db, create_app
from config import TestConfig
from web.models import Character, User


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

        yield empty_client
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    with app.app_context():
        client = app.test_client()
        db.create_all()

        password = generate_password_hash('Monday1')
        db.session.add(User(id=1, first_name='Test', last_name='User', email='someone@noplace.com', password=password))
        db.session.commit()

        data = dict(email='someone@noplace.com', password='Monday1', remember_me=False)
        client.post('/login', data=data)

        yield client
        db.drop_all()


@pytest.fixture(scope='function')
def client_loaded(app):
    with app.app_context():
        client_loaded = app.test_client()
        db.create_all()

        password = generate_password_hash('Monday1')
        db.session.add(User(id=1, first_name='Test', last_name='User', email='someone@noplace.com', password=password))
        db.session.add(User(id=2, first_name='John', last_name='Smith', email='john@smith.com', password=password))
        db.session.commit()

        db.session.add(Character(id=1, name='Paladin', is_dead=False, user_id=1))
        db.session.add(Character(id=2, name='Rogue', is_dead=False, user_id=1))
        db.session.add(Character(id=3, name='Fighter', is_dead=False, user_id=2))
        db.session.commit()

        data = dict(email='john@smith.com', password='Monday1', remember_me=False)
        client_loaded.post('/login', data=data)

        yield client_loaded
        db.drop_all()


def test_get_characters_for_user(client_loaded):
    """ Get characters for logged in user """
    # arrange

    # act
    result = client_loaded.get('/character', follow_redirects=True)

    # assert
    assert b'Fighter' in result.data
    assert b'Rogue' not in result.data


def test_handle_no_character(client):
    # arrange

    # act
    result = client.get('/character', follow_redirects=True)

    # assert
    assert b'Characters' in result.data


def test_get_character_list(client):
    # arrange

    # act
    result = client.get('/character')

    # assert
    assert b'Add Character' in result.data


def test_add_character(client):
    # arrange

    # act
    client.post('/character/add', data=dict(name='Rogue', is_dead=False, user_id=1), follow_redirects=True)

    # assert
    char = Character.query.get(1)
    assert char.name == 'Rogue'
    assert char.is_dead is True


def test_check_character_listed(client):
    # arrange

    # act
    result = client.post('/character/add', data=dict(name='Ranger', is_dead=False), follow_redirects=True)

    # asert
    assert b'Ranger' in result.data


def test_edit_character_ok(client_loaded):
    # arrange

    # act
    data = dict(id=2, name='Wizard', is_dead=True)
    rv = client_loaded.post('/character/2', data=data, follow_redirects=True)

    # assert
    char = Character.query.get(2)
    assert char.name == 'Wizard'
    assert char.is_dead is True
    assert b'Add Character' in rv.data


def test_show_edit_character(client_loaded):
    # arrange

    # act
    rv = client_loaded.post('/character/2', follow_redirects=True)

    # assert
    assert b'Edit' in rv.data


def test_cancel_edit_character(client_loaded):
    # arrange
    client_loaded.post('/character/2', follow_redirects=True)

    # act
    rv = client_loaded.post('/character', follow_redirects=True)

    # assert
    assert b'Edit' not in rv.data


def test_edit_character_missingdata(client_loaded):
    # arrange

    # act
    data = dict(id=2, name='', is_dead=True)
    result = client_loaded.post('/character/2', data=data, follow_redirects=True)

    # assert
    assert b'Edit Character' in result.data
