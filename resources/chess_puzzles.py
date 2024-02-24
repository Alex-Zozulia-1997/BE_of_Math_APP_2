from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256 as sha256
from flask_cors import cross_origin
from flask import request
from random import randint, choice


from flask_jwt_extended import jwt_required, get_jwt

from models import ChessPuzzleModel
from schemas import ChessPuzzleSchema
from db import db


blp = Blueprint(
    "chess_puzzle",
    "chess_puzzle",
    url_prefix="/chess_puzzle",
    description="Operations on chess puzzle",
)


@blp.route("/all")
class AllGames(MethodView):
    @jwt_required()
    @blp.response(200, ChessPuzzleSchema(many=True))
    def get(self):
        return ChessPuzzleModel.query.all()


@blp.route("/random")
class Random(MethodView):
    @blp.response(200, ChessPuzzleSchema)
    def get(self):
        rating_min = request.args.get("min_rating", type=int, default=0)
        rating_max = request.args.get("max_rating", type=int, default=float("inf"))
        number_of_pieces = request.args.get(
            "number_of_pieces", type=int, default=float("inf")
        )

        puzzles = ChessPuzzleModel.query.filter(
            ChessPuzzleModel.rating.between(rating_min, rating_max),
            ChessPuzzleModel.number_of_pieces <= number_of_pieces,
        ).all()

        if puzzles:
            puzzle = choice(puzzles)
            return puzzle
        else:
            return {"error": "No puzzles found for the given criteria"}, 404
