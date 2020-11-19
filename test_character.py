from main import Character


def test_base():
    assert True


def test_create_character():
    char = Character()
    char.name = 'test'
    assert char.name == 'test'
