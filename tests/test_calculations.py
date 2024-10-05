from app.calculations import add

def test_add():
    print("Testing add function")
    assert add(5,3) == 8

test_add()