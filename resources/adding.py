from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256 as sha256
from flask_cors import cross_origin
import datetime
from flask import request
from resources.functions.percentile import calculate_percentiles


from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from flask_jwt_extended import jwt_required, get_jwt
from blocklist import BLOCKLIST

from models import AddingGameModel
from schemas import AddingGameSchema
from db import db


blp = Blueprint(
    "adding_game",
    "adding_game",
    url_prefix="/adding",
    description="Operations on adding game",
)


@blp.route("/all")
class AllGames(MethodView):
    @jwt_required()
    @blp.response(200, AddingGameSchema(many=True))
    def get(self):
        return AddingGameModel.query.all()


@blp.route("/new")
class AddGame(MethodView):
    @jwt_required()
    @blp.arguments(AddingGameSchema)
    def post(self, game_data):
        game = AddingGameModel(
            user_id=get_jwt_identity(),
            game_won=game_data["game_won"],
            game_time=game_data["game_time"],
            game_date=datetime.datetime.now(),
            number_of_digits=game_data["number_of_digits"],
            seconds=game_data["seconds"],
            actions=game_data["actions"],
            user_answer=game_data["user_answer"],
            correct_answer=game_data["correct_answer"],
        )
        db.session.add(game)
        db.session.commit()
        return {"message": "all is well, a new game is added"}


@blp.route("/stats")
class Stats(MethodView):
    @jwt_required()
    @blp.response(200, AddingGameSchema(many=True))
    def get(self):
        user_id = get_jwt_identity()
        return AddingGameModel.query.filter(AddingGameModel.user_id == user_id).all()


@blp.route("/percentile")
class Percentile(MethodView):
    @jwt_required()
    @blp.response(200)
    def get(self):
        user_id = get_jwt_identity()
        dict_of_per = calculate_percentiles(AddingGameModel, user_id)
        return dict_of_per
