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


def test_get_all_chess_games(client):
    access_token = get_token()
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get("/chess_game/all", headers=headers)

    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_add_new_chess_game(client):
    access_token = get_token()
    game_data = {
        "user_id": 3,
        "puzzle_id": 10,
        "game_won": True,
        "game_date": "2024-01-13T19:10:06.587729",
        "solving_time": 5,
        "user_answer": ";ksdfljh",
        "game_won": True,
    }

    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.post("/chess_game/new", json=game_data, headers=headers)

    assert response.status_code == 200
    data = json.loads(response.data)
    assert "message" in data
    assert data["message"] == "Game added successfully"


def test_get_chess_game_stats(client):
    access_token = get_token()
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get("/chess_game/stats", headers=headers)

    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_get_all_chess_puzzles(client):
    access_token = get_token()
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get("/chess_puzzle/all", headers=headers)

    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_get_random_chess_puzzle(client):
    access_token = get_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    query_params = {"min_rating": 1000, "max_rating": 2000, "number_of_pieces": 16}

    response = client.get(
        "/chess_puzzle/random", query_string=query_params, headers=headers
    )

    assert response.status_code in [200, 404]
    data = json.loads(response.data)
    if response.status_code == 200:
        assert "id" in data
    else:
        assert "error" in data
