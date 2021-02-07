""" Tests for user creation and login """
import pytest
from werkzeug.security import generate_password_hash, check_password_hash

from web import create_app, db
from web.models import User
from config import TestConfig


@pytest.fixture(scope='session')
def app():
    """ Application Ficture """
    app = create_app()
    config = TestConfig()
    app.config.from_object(config)
    return app


@pytest.fixture(scope='function')
def empty_client(app):
    """ Empty Fixture """
    with app.app_context():
        empty_client = app.test_client()
        db.create_all()

        yield empty_client
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """ Fixture with some basic data """
    with app.app_context():
        client = app.test_client()
        db.create_all()

        # Add an existing user
        db.session.add(User(
            id=1,
            first_name='Adam',
            last_name='Alpha',
            email='adam@gmail.com',
            password=generate_password_hash('Monday1', method='sha256')))
        db.session.commit()

        yield client
        db.drop_all()


def test_attempt_add_existing_user(client):
    """ user Exists, we should redirect to signup """
    # arrange

    # act
    form_data = dict(first_name='Adam', last_name='Alpha', email='adam@gmail.com', password='Monday1', confirm='Monday1')
    result = client.post('/signup', data=form_data, follow_redirects=True)

    # assert
    assert b'Signup' in result.data


def test_attempt_add_missing_data(client):
    """ missing data, we should redirect to signup """
    # arrange

    # act
    form_data = dict(first_name='Betty', email='betty@gmail.com', password='Monday1', confirm='Monday1')    
    result = client.post('/signup', data=form_data, follow_redirects=True)

    # assert
    assert b'Signup' in result.data


def test_add_user_ok(client):
    """ Ok user Add, redirect to login, data added """
    # arrange

    # act
    form_data = dict(first_name='Betty', last_name='Beta', email='betty@gmail.com', password='Monday1', confirm='Monday1')
    result = client.post('/signup', data=form_data, follow_redirects=True)

    # assert
    assert b'Login' in result.data
    user = User.query.filter_by(id=2).first()
    assert user is not None


def test_check_password_hash(client):
    """ Ok user Add, redirect to login, data added """
    # arrange

    # act
    form_data = dict(first_name='Betty', last_name='Beta', email='betty@gmail.com', password='Monday1', confirm='Monday1')
    client.post('/signup', data=form_data, follow_redirects=True)

    # assert
    user = User.query.filter_by(id=2).first()
    assert check_password_hash(user.password, b'Monday1')
