import pytest
from app import create_app
from flask import json
from utils.utils_for_tests import get_token

last_number = 0


@pytest.fixture()
def app():
    app = create_app("sqlite:///data.db")
    app.config["TESTING"] = True
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_get_all_users(client):
    access_token = get_token()
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get("/users", headers=headers)

    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_double_new_user(client):
    access_token = get_token()
    data = {"username": "nadia@nekrysa.com", "password": "12345678a"}

    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.post("/register", json=data, headers=headers)

    assert response.status_code == 409
    data = json.loads(response.data)
    assert "message" in data
    assert data["message"] == "A user with that username already exists"


def test_delete_new_user(client):
    access_token = get_token()
    headers = {"Authorization": f"Bearer {access_token}"}

    added_user_ids = client.get("/users", headers=headers).json
    print(added_user_ids)
    added_un = "101nadia@nekrysa.com"
    for i in added_user_ids:
        if i["username"] == added_un:
            deleting_id = i["id"]
    response = client.delete(f"/user/{deleting_id}", headers=headers)

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == f"User with id {deleting_id} is out"


def test_add_new_user(client):
    access_token = get_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"username": "101nadia@nekrysa.com", "password": "12345678a"}

    response = client.post("/register", json=data, headers=headers)

    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert data["message"] == "all is well, a new user is added"
