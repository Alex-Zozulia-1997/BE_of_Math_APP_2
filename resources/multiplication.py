from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256 as sha256
from flask_cors import cross_origin
import datetime
from flask import request
from utils.percentiles import *

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from flask_jwt_extended import jwt_required, get_jwt
from blocklist import BLOCKLIST

from models import MultiplicationGameModel
from schemas import MuiltplyGameSchema
from db import db


blp = Blueprint(
    "multiplication_game",
    "multiplication_game",
    url_prefix="/multiplication",
    description="Operations on multiplication game",
)


@blp.route("/all")
class AllGames(MethodView):
    @jwt_required()
    @blp.response(200, MuiltplyGameSchema(many=True))
    def get(self):
        return MultiplicationGameModel.query.all()


@blp.route("/new")
class AddGame(MethodView):
    @jwt_required()
    @blp.arguments(MuiltplyGameSchema)
    def post(self, game_data):
        game = MultiplicationGameModel(
            user_id=get_jwt_identity(),
            game_won=game_data["game_won"],
            game_date=datetime.datetime.now(),
            total_number_of_digits=game_data["total_number_of_digits"],
            multiplication_time=game_data["multiplication_time"],
            user_answer=game_data["user_answer"],
            correct_answer=game_data["correct_answer"],
        )
        db.session.add(game)
        db.session.commit()
        return {"message": "all is well, a new game is added"}


@blp.route("/stats")
class Stats(MethodView):
    @jwt_required()
    @blp.response(200, MuiltplyGameSchema(many=True))
    def get(self):
        user_id = get_jwt_identity()
        return MultiplicationGameModel.query.filter(
            MultiplicationGameModel.user_id == user_id
        ).all()


@blp.route("/percentile")
class Percentile(MethodView):
    @jwt_required()
    @blp.response(200)
    def get(self):
        user_id = get_jwt_identity()
        percentiles = []
        for attribute in ["total_number_of_digits"]:
            avgs = get_all_users_averages(MultiplicationGameModel, attribute)
            percentile = calculate_percentile(user_id, avgs)
            percentiles.append({attribute: percentile})

        totals = get_all_users_totals(MultiplicationGameModel, "multiplication_time")
        print(totals)
        game_time_percentile = calculate_percentile(user_id, totals)
        percentiles.append({"multiplication_time": game_time_percentile})

        # Success
        s_rates = get_all_users_success_rates(MultiplicationGameModel)
        print(get_all_users_success_rates(MultiplicationGameModel))
        success_percentile = calculate_percentile(user_id, s_rates)
        percentiles.append({"success_rate": success_percentile})

        dict_of_per = {}
        for d in percentiles:
            dict_of_per.update(d)
        return dict_of_per
