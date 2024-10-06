import pytest
from app import schemas
from jose import jwt
from app.config import settings

def test_root(client):
    response = client.get("/")
    print(response.json().get('message'))
    assert response.json().get('message') == "Hello World"
    assert response.status_code == 200

def test_create_user(client):
    response = client.post("/users/",json={"email":"dhoni1@gmail.com","password":"5cups"})
    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == "dhoni1@gmail.com"
    assert response.status_code == 201

def test_login_user(client, test_user):
    response = client.post("/login",data={"username":test_user['email'],"password":test_user['password']})
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token,settings.secret_key,algorithms=[settings.algorithm])
    id= payload.get("user_id")
    assert id == test_user['id']
    assert login_response.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize("email,password,status_code",[
    ("wrong@gmail.com","ds",403),
    ("dhoni1@gmail.com","5cu",403)
])
def test_incorrect_login(client,test_user,email,password,status_code):
    response = client.post("/login",data={"username":email,"password":password})
    assert response.status_code == status_code
    #assert response.json().get('detail') == "Invalid Credentials"