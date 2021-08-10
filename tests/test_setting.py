""" Tests for setting utility """
import pytest

from config import TestConfig
from web import db, create_app
from web.models import Character, Setting
from web.utility.setting import get_setting, save_setting


@pytest.fixture(scope='session')
def app():
    app = create_app()
    config = TestConfig()
    app.config.from_object(config)
    return app


@pytest.fixture(scope='function')
def client(app):
    with app.app_context():
        client = app.test_client()
        db.create_all()

        # Add settings
        db.session.add(Setting(id=1, key='test_session', value='1'))

        # Add some Characters
        db.session.add(Character(id=1, name='Paladin', is_dead=False))
        db.session.add(Character(id=2, name='Rogue', is_dead=False))
        db.session.add(Character(id=3, name='Fighter', is_dead=False))
        db.session.commit()

        yield client
        db.drop_all()


def test_get_setting(client):
    # arrange

    # act
    with client.application.test_request_context('/'):
        result = get_setting('test_session')

        # assert
        assert result == '1'


def test_save_setting(client):
    # arrange

    # act
    with client.application.test_request_context('/'):
        save_setting('warp_flux', '21')

    # assert
    result = Setting.query.filter_by(key='warp_flux').first()
    assert result.value == '21'


def test_update_setting(client):
    # arrange
    with client.application.test_request_context('/'):
        save_setting('third_setting', 'Alpha')

    # act
        save_setting('third_setting', 'Beta')

    # assert
        assert get_setting('third_setting') == 'Beta'


def test_create_entry_save_game_session(client):
    """ Add an entry and check that the game_session is saved """
    # arrange

    # act
    data = dict(game_session=2300, description='Wand of Heal', amount=10.02, entry_type='withdrawl')
    with client.application.test_request_context('/'):
        result = client.post('/entry/add', data=data, follow_redirects=True)

    # assert
        result = get_setting('game_session')
        assert result == '2300'


def test_get_a_setting_default(client):
    """ Test that we can get a default value for a setting """
    # arrange

    # act
    with client.application.test_request_context('/'):
        result = get_setting('warp_factor', '4')

    # assert
        assert result == '4'


# def test_index_loads_game_session(client):
#     # arrange
#     with client.application.test_request_context('/'):

#         # set the game session
#         save_setting('game_session', '21999')

#         # act
#         # get the index page, does it contain the session
#         result = client.get('/')

#         # assert
#         assert b'21999' in result.data
