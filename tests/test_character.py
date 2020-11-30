""" Tests related to CRUD operations for Characters """
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
        yield client
        db.drop_all()


@pytest.fixture
def client_loaded():
    config = TestConfig()
    app.config.from_object(config)

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        db.session.add(Character(id=1, name='Paladin', is_dead=False))
        db.session.add(Character(id=2, name='Rogue', is_dead=False))
        db.session.add(Character(id=3, name='Fighter', is_dead=False))
        yield client
        db.drop_all()


def test_create_character():
    char = Character()
    char.name = 'test'
    assert char.name == 'test'


def test_get_character_list(client):
    rv = client.get('/character')
    assert b'Add Character' in rv.data


def test_add_character(client):
    # arrange

    # act
    client.post('/character/add', data=dict(name='Rogue', is_dead=False), follow_redirects=True)

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
    result = client_loaded.post('/character/2', data=data, follow_redirects=True)

    # assert
    char = Character.query.get(2)
    assert char.name == 'Wizard'
    assert char.is_dead is True
    assert b'Add Character' in result.data


def test_edit_character_missingdata(client_loaded):
    # arrange

    # act
    data = dict(id=2, name='', is_dead=True)
    result = client_loaded.post('/character/2', data=data, follow_redirects=True)

    # assert
    assert b'Edit Character' in result.data
