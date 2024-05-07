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


def test_login(client):
    user_data = {"username": "nadia@nekrysa.com", "password": "12345678a"}
    response = client.post("/login", json=user_data)

    assert response.status_code == 200


def test_wrong_login_credentials(client):
    user_data = {"username": "nadia@nekrysa.com11111", "password": "12345678a"}
    response = client.post("/login", json=user_data)
    assert response.status_code == 401


def test_logout(client):
    access_token = get_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    user_data = {"username": "nadia@nekrysa.com", "password": "12345678a"}
    response = client.post("/logout", json=user_data, headers=headers)

    assert response.status_code == 200
