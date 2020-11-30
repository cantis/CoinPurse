""" Tests involved in CRUD for transaction Entries """
import pytest

from config import TestConfig
from main import app, db, Entry, Character


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

        yield client
        db.drop_all()


def test_create_entry():
    # arrange

    # act
    ent = Entry()
    ent.description = 'Test Entry'

    # assert
    # assert ent.description == 'Test Entry'


# def test_add_transaction_ok(client):
#     # arrange
#     data = dict(select_character=1, session=1, description="Wand of Healing", amount=-750.00)

#     # act
#     result = client.post('/add', data=data, follow_redirects=True)

#     # assert
#     ent = Entry().query.get(1)
#     assert ent.description == 'Wand of Healing'
#     assert ent.amount == -750.00
#     assert ent.character_id == 10
#     assert ent.session == 1
#     assert b'Add Entry' in result.data
