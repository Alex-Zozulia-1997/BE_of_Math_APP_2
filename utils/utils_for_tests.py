import requests


def get_token():
    response = requests.post(
        "http://127.0.0.1:5000/login",
        json={"username": "salex@alex.comii", "password": "12345678a"},
    )

    print(response.status_code)
    token = response.json()["access_token"]
    return token
