import unittest
from app import create_app
from flask import json
from utils.utils_for_tests import get_token


class TestAuthRoutes(unittest.TestCase):

    def setUp(self):
        self.app = create_app("sqlite:///data.db")
        self.app.config["TESTING"] = True
        self.app.config["JWT_SECRET_KEY"] = 263439876012693437083642831966594211143
        self.client = self.app.test_client()

    def test_login(self):
        user_data = {"username": "nadia@nekrysa.com", "password": "12345678a"}
        response = self.client.post("/login", json=user_data)
        self.assertEqual(response.status_code, 200)

    def test_wrong_login_credentials(self):
        user_data = {"username": "nadia@nekrysa.com11111", "password": "12345678a"}
        response = self.client.post("/login", json=user_data)
        self.assertEqual(response.status_code, 401)

    def test_logout(self):
        access_token = get_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        user_data = {"username": "nadia@nekrysa.com", "password": "12345678a"}
        response = self.client.post("/logout", json=user_data, headers=headers)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
