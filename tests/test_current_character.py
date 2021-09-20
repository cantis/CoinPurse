""" Tests for setting the currently selected character """
import pytest
from web import db, create_app
from werkzeug.security import generate_password_hash
from config import TestConfig
from web.models import Character, Setting, User


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

        # Still need some users to be able to login
        password = generate_password_hash('Monday1')
        db.session.add(User(id=1, first_name='Test', last_name='User', email='someone@noplace.com', password=password))
        db.session.add(User(id=2, first_name='TestB', last_name='UserTwo', email='noone@noplace.com', password=password))
        db.session.commit()

        yield empty_client

        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    with app.app_context():
        client = app.test_client()
        __init_test_db()

        yield client
        db.drop_all()


def __init_test_db():
    db.create_all()

    # Add Users
    password = generate_password_hash('Monday1')
    db.session.add(User(id=1, first_name='TestA', last_name='UserOne', email='someone@noplace.com', password=password))
    db.session.add(User(id=2, first_name='TestB', last_name='UserTwo', email='noone@noplace.com', password=password))
    db.session.commit()

    db.session.add(Character(id=1, user_id=1, name='Paladin', is_dead=False))
    db.session.add(Character(id=2, user_id=1, name='Rogue', is_dead=False))
    db.session.add(Character(id=3, user_id=2, name='Fighter', is_dead=False))
    db.session.commit()


def test_set_current_character(client):
    with client:
        # arrange
        client.post('/login', data=dict(email='noone@noplace.com', password='Monday1', remember_me=False))
        character_id = 2

        # act
        rv = client.post('/current_character', data=dict(selected_character=character_id), follow_redirects=True)

        # assert
        assert rv.status_code == 200


def test_current_character_no_db_no_records(empty_client):
    with empty_client:
        # arrange
        empty_client.post('/login', data=dict(email='noone@noplace.com', password='Monday1', remember_me=False))

        # act
        rv = empty_client.get('/entry', follow_redirects=True)

        # assert
        assert b'Characters' in rv.data
        assert b'Add Character' in rv.data


def test_current_character_not_set(client):
    """ Get the current character, with none set """
    with client:
        # arrange
        client.post('/login', data=dict(email='someone@noplace.com', password='Monday1', remember_me=False))

        # act
        rv = client.get('/entry', follow_redirects=True)

        # assert
        assert b'Paladin' in rv.data


def test_saved_character_setting(client):
    """ get_current_character from Settings table """
    with client:
        # arrange
        client.post('/login', data=dict(email='noone@noplace.com', password='Monday1', remember_me=False))
        character_id = 3
        client.post('/current_character', data=dict(selected_character=character_id), follow_redirects=True)

        # act
        rv = client.get('/entry')

        # assert
        assert b'Fighter' in rv.data


def test_check_setting_saved(client):
    """ Check that the setting is saved to the table when it's changed """
    with client:
        # arrange
        client.post('/login', data=dict(email='noone@noplace.com', password='Monday1', remember_me=False))
        db.session.add(Setting(key='current_character', value='2'))
        db.session.commit()

        # act
        character_id = 3
        client.post('/current_character', data=dict(selected_character=character_id), follow_redirects=True)

        # assert
        current_character = Setting.query.filter_by(key='current_character').first()
        assert current_character.value == '3'


def test_get_current_character_id(client):
    with client:
        # arrange
        client.post('/login', data=dict(email='someone@noplace.com', password='Monday1', remember_me=False))
        db.session.add(Setting(key='current_character', value='2'))
        db.session.commit()

        # act
        rv = rv = client.get('/entry', follow_redirects=True)

        # assert
        assert b'Rogue' in rv.data
