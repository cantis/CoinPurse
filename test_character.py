import pytest

from main import app, db, Character, AddCharacterForm
from config import TestConfig


@pytest.fixture
def client():
    config = TestConfig()
    app.config.from_object(config)

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_create_character():
    char = Character()
    char.name = 'test'
    assert char.name == 'test'


def test_get_character_list(client):
    rv = client.get('/character')
    assert b'Add Character' in rv.data


def test_add_character(client):
    client.post('/character/add', data=dict(name='test', is_dead=False), follow_redirects=True)
    char = Character.query.get(1)
    assert char.name == 'test'
    assert char.is_dead is True


def test_check_character_listed(client):
    rv = client.post('/character/add', data=dict(name='peanut', is_dead=False), follow_redirects=True)
    assert b'peanut' in rv.data
