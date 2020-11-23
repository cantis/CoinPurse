import pytest

from main import app, db, Character, get_current_character, blank_current_character, set_current_character
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


# @pytest.fixture(autouse=True)
# def client_reset(client):
#     db.drop_all()


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
    assert char is None


def test_change_current_character(client):
    # arrange
    blank_current_character()
    db.session.add(Character(id=1, name='Paladin', is_dead=False))
    db.session.add(Character(id=2, name='Rogue', is_dead=False))
    db.session.add(Character(id=3, name='Fighter', is_dead=False))
    set_current_character(2)

    # act
    client.post('/change_character', data=dict(select_character='3'), follow_redirects=True)

    # assert
    result = get_current_character()
    assert result.name == 'Fighter'


def test_set_current_character(client):
    # arrange
    blank_current_character()
    db.session.add(Character(id=1, name='Paladin', is_dead=False))
    db.session.add(Character(id=2, name='Rogue', is_dead=False))
    db.session.add(Character(id=3, name='Fighter', is_dead=False))

    # act
    set_current_character(2)

    # assert
    result = get_current_character()
    assert result.name == 'Rogue'


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
