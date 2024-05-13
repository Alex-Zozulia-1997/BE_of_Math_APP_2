import pytest
import sys

sys.path.insert(1, "..")
from app import create_app
from flask import json
from models import UserModel

from flask_jwt_extended import create_access_token, JWTManager

import os
import dotenv

dotenv.load_dotenv()


@pytest.fixture()
def app():
    app = create_app("sqlite:///:memory:")
    app.config["TESTING"] = True
    app.config["JWT_SECRET_KEY"] = os.getenv(
        "SK", "263439876012693437083642831966594211143"
    )
    jwt = JWTManager(app)
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
