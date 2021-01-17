""" Tests for setting utility """
import pytest

from config import TestConfig
from app import db, create_app
from app.setting.models import Setting
from app.setting.utility import get_setting, save_setting


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
        db.session.add(Setting(id=1, key='last_session', value="1"))

        yield client
        db.drop_all()


def test_get_setting(client):
    # arrange

    # act
    result = get_setting('last_session')

    # assert
    assert result.value == '1'


def test_save_setting(client):
    # arrange

    # act
    save_setting('warp_flux', '21')

    # assert
    result = Setting.query.filter_by(key='warp_flux').first()
    assert result.value == '21'
