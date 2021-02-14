""" Tests related to CRUD operations for Characters """
import pytest
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

        try:
            db.session.add(User(id=1, first_name='Test', last_name='User', email='someone@noplace.com', password='Monday1'))
            db.session.commit()
        except Exception as e:
            print(e.message)

        yield client
        db.drop_all()


@pytest.fixture(scope='function')
def client_loaded(app):
    with app.app_context():
        client_loaded = app.test_client()
        db.create_all()

        db.session.add(User(id=1, first_name='Test', last_name='User', email='someone@noplace.com', password='Monday1'))
        db.session.commit()

        db.session.add(Character(id=1, name='Paladin', is_dead=False, user_id=1))
        db.session.add(Character(id=2, name='Rogue', is_dead=False, user_id=1))
        db.session.add(Character(id=3, name='Fighter', is_dead=False, user_id=1))
        db.session.commit()

        yield client_loaded
        db.drop_all()


def test_handle_no_character(empty_client):
    # arrange

    # act
    result = empty_client.get('/character', follow_redirects=True)

    # assert
    assert b'Characters' in result.data


def test_create_character():
    # arrange
    char = Character()

    # act
    char.name = 'test'

    # assert
    assert char.name == 'test'


def test_get_character_list(client):
    # arrange

    # act
    rv = client.get('/character')

    # assert
    assert b'Add Character' in rv.data


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
    rv = client.post('/character/add', data=dict(name='Ranger', is_dead=False), follow_redirects=True)

    # asert
    assert b'Ranger' in rv.data


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
