from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
import models
import secrets
from blocklist import BLOCKLIST
from datetime import timedelta
from dotenv import load_dotenv
import os


from db import db

from resources.user import blp as UserBlueprint
from resources.adding import blp as AddingBlueprint
from resources.multiplication import blp as MultiplicationBlueprint
from resources.chess_puzzles import blp as ChessPuzzleBlueprint
from resources.chess_game import blp as ChessGameBlueprint

load_dotenv()


def create_app(db_url=os.getenv("DATABASE_URL")):
    app = Flask(__name__)
    CORS(app)
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

    db.init_app(app)
    migrate = Migrate(app, db, render_as_batch=True)
    api = Api(app)
    app.config["JWT_SECRET_KEY"] = os.getenv("SK")
    jwt = JWTManager(app)

    @jwt.invalid_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token has expired, because you are a slow mother fucheker",
                    "error": "token_expired",
                }
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token, maaaan",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    #
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token has been revoked, because you logged out mother fucheker",
                    "error": "token_revoked",
                }
            ),
            401,
        )

    with app.app_context():
        db.create_all()

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(AddingBlueprint)
    api.register_blueprint(MultiplicationBlueprint)
    api.register_blueprint(ChessPuzzleBlueprint)
    api.register_blueprint(ChessGameBlueprint)
    return app
