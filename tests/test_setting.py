""" Tests for setting utility """
import pytest
from werkzeug.security import generate_password_hash

from config import TestConfig
from web import db, create_app
from web.models import Character, Setting, User, Entry
from web.utility.setting import get_setting, save_setting


@pytest.fixture(scope='session')
def app():
    ''' Set test App context '''
    app = create_app()
    config = TestConfig()
    app.config.from_object(config)
    return app


@pytest.fixture(scope='function')
def client(app):
    ''' Create test context '''
    with app.app_context():
        client = app.test_client()

        __init_test_db()

        yield client

        db.drop_all()


def __init_test_db():
    ''' Add mock db data '''
    db.create_all()

    # Add Users
    password = generate_password_hash('Monday1')
    db.session.add(User(id=1, first_name='TestA', last_name='UserOne', email='someone@noplace.com', password=password))
    db.session.add(User(id=2, first_name='TestB', last_name='UserTwo', email='noone@noplace.com', password=password))
    db.session.commit()

    # Add sessions
    db.session.add(Setting(id=1, user_id=1, key='test_session', value='42'))
    db.session.add(Setting(id=2, user_id=2, key='test_session', value='99'))

    # Add some Characters
    db.session.add(Character(id=1, user_id=1, name='Paladin', is_dead=False))
    db.session.add(Character(id=2, user_id=1, name='Rogue', is_dead=False))
    db.session.add(Character(id=3, user_id=2, name='Fighter', is_dead=False))
    db.session.commit()

    # Add some entries
    db.session.add(Entry(id=1, game_session=1, description='Wand', amount=10.00, character_id=1))
    db.session.add(Entry(id=2, game_session=1, description='Sword', amount=20.00, character_id=1))
    db.session.add(Entry(id=3, game_session=2, description='Potion', amount=30.00, character_id=1))
    db.session.add(Entry(id=4, game_session=1, description='Crossbow', amount=40.00, character_id=2))
    db.session.add(Entry(id=5, game_session=1, description='Spear', amount=50.00, character_id=2))
    db.session.add(Entry(id=6, game_session=2, description='Backpack', amount=60.00, character_id=2))
    db.session.commit()


def test_get_setting_user_one(client):
    ''' Session number for User 1'''
    with client:
        # arrange
        client.post('/login', data=dict(email='someone@noplace.com', password='Monday1', remember_me=False))

        # act
        result = get_setting('test_session')

        # assert
        assert result == '42'


def test_get_session_user_two(client):
    ''' Session number for User 2'''
    with client:
        # arrange
        client.post('/login', data=dict(email='noone@noplace.com', password='Monday1', remember_me=False))

        # act
        result = get_setting('test_session')

        # assert
        assert result == '99'


def test_save_setting(client):
    ''' Confirm a setting is saved '''
    with client:
        # arrange
        client.post('/login', data=dict(email='someone@noplace.com', password='Monday1', remember_me=False))

        # act
        save_setting('warp_flux', '21')

        # assert
        result = Setting.query.filter_by(key='warp_flux').first()
        assert result.value == '21'


def test_update_setting(client):
    with client:
        # arrange
        client.post('/login', data=dict(email='someone@noplace.com', password='Monday1', remember_me=False))
        save_setting('third_setting', 'Alpha')

        # act
        save_setting('third_setting', 'Beta')

        # assert
        assert get_setting('third_setting') == 'Beta'


def test_create_entry_save_game_session(client):
    """ Add an entry and check that the game_session is saved """
    with client:
        # arrange
        client.post('/login', data=dict(email='someone@noplace.com', password='Monday1', remember_me=False))

        # act
        data = dict(game_session=2300, description='Wand of Heal', amount='10.02', entry_type='withdrawl')
        result = client.post('/entry/add', data=data, follow_redirects=True)

        # assert
        result = get_setting('game_session')
        assert result == 2300


def test_get_a_setting_default(client):
    """ Test that we can get a default value for a setting """
    with client:
        # arrange
        client.post('/login', data=dict(email='someone@noplace.com', password='Monday1', remember_me=False))

        # act
        result = get_setting('warp_factor', '4')

        # assert
        assert result == '4'


def test_index_loads_game_session(client):
    # arrange
    with client:
        # arrange
        client.post('/login', data=dict(email='someone@noplace.com', password='Monday1', remember_me=False))
        db.session.add(Entry(id=7, game_session=21999, description='Power Staff', amount=1130.00, character_id=1))
        db.session.commit()
        save_setting('filter_game_session', '21999', )

        # act
        # get the index page, does it contain the session
        result = client.get('/')

        # assert
        assert b'21999' in result.data
