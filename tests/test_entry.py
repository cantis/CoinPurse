""" Tests involved in CRUD for transaction Entries """
import pytest

from config import TestConfig
from main import app, db, Entry, Character, Setting


@pytest.fixture
def client(scope='function'):
    config = TestConfig()
    app.config.from_object(config)

    with app.test_client() as client:
        # Create the Database
        with app.app_context():
            db.create_all()
        # Add some Characters
        db.session.add(Character(id=1, name='Paladin', is_dead=False))
        db.session.add(Character(id=2, name='Rogue', is_dead=False))
        db.session.add(Character(id=3, name='Fighter', is_dead=False))
        db.session.commit()

        # Set the current Character
        db.session.add(Setting(key='current_character', value='2'))
        db.session.commit()

        yield client
        db.drop_all()


def test_create_entry(client):
    assert True
    
    # client.post('/current_character', data=dict(selected_character=character_id), follow_redirects=True)
