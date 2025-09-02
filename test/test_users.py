import pytest
from jose import jwt
from app import schemas
from app.config import settings


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "omogbolahan@gmail.com", "password": "password123", "id": 1})

    print(res.json())
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "omogbolahan@gmail.com"
    assert res.status_code == 201


def test_login_user(test_user_exist, client):
    res = client.post(
        "/login", data={"username": test_user_exist['email'], "password": test_user_exist['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    id = payload.get("user_id")
    assert id == test_user_exist['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
