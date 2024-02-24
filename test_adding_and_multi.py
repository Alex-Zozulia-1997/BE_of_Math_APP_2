import pytest
from app import create_app
from flask import json
from utils.utils_for_tests import get_token


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


def test_get_all_games(client):
    access_token = get_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    response = client.get("/adding/all", headers=headers)

    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_add_new_game(client):
    access_token = get_token()
    game_data = {
        "user_id": 3,
        "game_won": True,
        "game_time": 45,
        "number_of_digits": 4,
        "game_date": "2024-01-13T19:10:06.587729",
        "seconds": 215,
        "actions": 10,
        "user_answer": 1234,
        "correct_answer": 432,
    }

    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.post("/adding/new", json=game_data, headers=headers)

    assert response.status_code == 200
    data = json.loads(response.data)
    assert "message" in data
    assert data["message"] == "all is well, a new game is added"


def test_get_stats(client):
    access_token = get_token()

    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get("/adding/stats", headers=headers)

    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_get_all_multiplication_games(client):
    access_token = get_token()
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get("/multiplication/all", headers=headers)

    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_add_new_multiplication_game(client):
    access_token = get_token()
    game_data = {
        "user_id": 3,
        "game_won": True,
        "total_number_of_digits": 4,
        "game_date": "2024-01-13T19:10:06.587729",
        "muliplication_time": 215,
        "user_answer": 1234,
        "correct_answer": 432,
    }

    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.post("/multiplication/new", json=game_data, headers=headers)

    assert response.status_code == 200
    data = json.loads(response.data)
    assert "message" in data
    assert data["message"] == "all is well, a new game is added"


def test_get_multiplication_stats(client):
    access_token = get_token()

    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get("/multiplication/stats", headers=headers)

    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
