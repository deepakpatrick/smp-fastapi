from app import schemas
from jose import jwt
from app.config import settings
import pytest

def test_root(client):
    response = client.get("/")
    print(response.json().get('message'))
    assert response.json().get('message') == "SMP Fastapi - deployed from CI/CD"
    assert response.status_code == 200

def test_create_user(client):
    response = client.post("/users/", json={"email":"he214@g.com","password":"vvv"})
    print(response.json())
    response_user = schemas.UserCreateResponses(**response.json())
    assert response.status_code == 201
    assert response.json().get("email") == "he214@g.com"
    assert response_user.email == "he214@g.com"

def test_login_user(client, test_user):
    response = client.post("/login",data={"username":test_user['email'],"password":test_user['password']})
    print(response.json())
    login_response = schemas.Token(**response.json())
    decoded_token = jwt.decode(token=login_response.access_token, 
                             key=settings.secret_key, 
                             algorithms=[settings.algorithm])
    user_id: str = decoded_token.get("user_id")
    assert user_id == test_user['id']
    assert login_response.token_type == 'bearer'
    assert response.status_code == 200



@pytest.mark.parametrize("email, password, status_code",[
    ('wrongemail@g.com','vvv',403),
    ('he214@g.com','wrongpassword',403),
    ('wrongemail@g.com','wrongpassword',403),
    ('he214@g.com', None, 422),
    (None, 'wrongpassword', 422),
])
def test_incorrect_login(client, test_user, email, password, status_code):
    response = client.post("/login",data={"username":email,"password":password})
    assert response.status_code == status_code
    