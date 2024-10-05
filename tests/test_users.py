from fastapi.testclient import TestClient
from app.main import app
from app import schemas

client = TestClient(app)

def test_root():
    response = client.get("/")
    print(response.json().get('message'))
    assert response.json().get('message') == "Hello World"
    assert response.status_code == 200

def test_create_user():
    response = client.post("/users/",json={"email":"dhoni1@gmail.com","password":"5cups"})
    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == "dhoni1@gmail.com"
    assert response.status_code == 201

