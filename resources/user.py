from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256 as sha256
from flask_cors import cross_origin
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from flask_jwt_extended import jwt_required, get_jwt
from blocklist import BLOCKLIST

from models import UserModel, AddingGameModel
from schemas import UserSchema, AddingGameSchema
from db import db

blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/register")
class Register(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists")
        user = UserModel(
            username=user_data["username"], password=sha256.hash(user_data["password"])
        )
        db.session.add(user)
        db.session.commit()
        return {"message": "all is well, a new user is added"}


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": f"User with id {user_id} is out"}


@blp.route("/users")
class Users(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()


@blp.route("/login")
class Login(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}
        else:
            abort(401, message="Invalid credentials")


@blp.route("/refresh")
class Refresh(MethodView):
    @jwt_required(refresh=True)
    def post(slef):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}


@blp.route("/logout")
class Logout(MethodView):
    @cross_origin()
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out, ma boi"}
