import pytest

from main import app, db, Character, get_current_character, blank_current_character
from config import TestConfig


@pytest.fixture
def client():
    config = TestConfig()
    app.config.from_object(config)

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
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


def test_get_current_character(client):
    """ Get the current character, with none set but at lease one Caracter Created """
    # arrange
    blank_current_character()
    db.session.add(Character(name='Paladin', is_dead=False))
    db.session.commit()

    # act
    char = get_current_character()

    # assert
    assert char.name == 'Paladin'


def test_current_character_none(client):
    """ Get the current character, with none set and none created """
    # arrange
    blank_current_character()

    # act
    char = get_current_character()

    # assert
    assert char.name == '*AddNew*'
