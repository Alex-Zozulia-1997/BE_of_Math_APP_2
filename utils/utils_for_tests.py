import requests

import os


def get_token():
    base_url = os.getenv("TEST_BASE_URL", "http://127.0.0.1:5000")
    response = requests.post(
        f"{base_url}/login",
        json={"username": "salex@alex.comii", "password": "12345678a"},
    )
    print(response.status_code)
    token = response.json()["access_token"]
    return token
