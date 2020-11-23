import pytest

from main import app, db, Entry
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


def test_create_entry():
    # arrange

    # act
    ent = Entry()
    ent.description = 'Test Entry'

    # assert
    assert ent.description == 'Test Entry'


def test_add_transaction_ok(client):
    # arrange
    data = dict(id=2, session=1, description="Wand of Healing", amount=-750.00)

    # act
    result = client.post('/add', data, follow_redirects=True)

    # assert
    ent = Entry().query.get(1)
    assert ent.description == 'Wand of Healing'
    assert ent.amount == -750.00
    assert b'Add Entry' in result.data
    assert b'Transactions' in result.data
