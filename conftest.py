import pytest
from app import create_app
from flask import json
from models import UserModel
from random import randint
from flask import current_app
from flask_jwt_extended import create_access_token, JWTManager

some_number = randint(0, 100)
import os
import dotenv

dotenv.load_dotenv()


@pytest.fixture()
def app():
    app = create_app("sqlite:///data.db")
    app.config["TESTING"] = True
    app.config["JWT_SECRET_KEY"] = os.getenv("SK")
    jwt = JWTManager(app)
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_register_user(client):
    user_data = {
        "username": f"bestuse9r@{some_number}users.com",
        "password": "password123",
    }
    response = client.post("/register", json=user_data)
    assert response.status_code == 200
    assert json.loads(response.data) == {"message": "all is well, a new user is added"}


def test_double_registration(client):
    user_data = {
        "username": f"nadia@nekrysa.com",
        "password": "password123",
    }
    response = client.post("/register", json=user_data)
    assert response.status_code == 409


def test_login_user(client):
    user_data = {
        "username": f"bestuse9r@{some_number}users.com",
        "password": "password123",
    }
    response = client.post("/login", json=user_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "access_token" in data
    assert "refresh_token" in data


def test_fake_login(client):
    user_data = {
        "username": f"estuse9r@users.com",
        "password": "password123",
    }
    response = client.post("login", json=user_data)
    assert response.status_code == 401


def test_logout(client):
    user_data = {
        "username": f"bestuse9r@{some_number}users.com",
        "password": "password123",
    }
    response = client.post("login", json=user_data)
    data = json.loads(response.data)
    token = data["access_token"]
    response_logout = client.post(
        "logout", headers={"Authorization": f"Bearer {token}"}
    )
    assert response_logout.status_code == 200
    assert json.loads(response_logout.data) == {
        "message": "Successfully logged out, ma boi"
    }


def test_get_users(client):
    user_data = {
        "username": f"bestuser@{some_number}users.com",
        "password": "password123",
    }
    response_register = client.post("/register", json=user_data)
    assert response_register.status_code == 200

    response_login = client.post("/login", json=user_data)
    assert response_login.status_code == 200
    data = json.loads(response_login.data)
    access_token = data["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    response_get_users = client.get("/users", headers=headers)

    assert response_get_users.status_code == 200
    user_list = json.loads(response_get_users.data)
    assert isinstance(user_list, list)


def test_cleanup_users(client):
    user_data = {
        "username": f"bestuser@{some_number}users.com",
        "password": "password123",
    }
    for i in range(4, 100):
        response_login = client.post("/login", json=user_data)
        assert response_login.status_code == 200
        data = json.loads(response_login.data)
        access_token = data["access_token"]

        headers = {"Authorization": f"Bearer {access_token}"}
        resp = client.delete(f"/user/{i}", headers=headers)
        assert resp.status_code == 401
