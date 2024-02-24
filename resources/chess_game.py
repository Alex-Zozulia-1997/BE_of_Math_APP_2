from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
from sqlalchemy.orm import joinedload


from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.percentiles import (
    get_user_average,
    get_all_users_averages,
    calculate_percentile,
    get_user_success_rate,
    get_all_users_success_rates,
    get_user_total,
    get_all_users_totals,
)
from models import ChessGameModel, ChessPuzzleModel
from schemas import ChessGameSchema, ChessPuzzleSchema
from db import db


blp = Blueprint(
    "chess_game",
    "chess_game",
    url_prefix="/chess_game",
    description="Operations on chess results",
)


@blp.route("/all")
class AllGames(MethodView):
    @jwt_required()
    @blp.response(200, ChessGameSchema(many=True))
    def get(self):
        return ChessGameModel.query.all()


@blp.route("/new")
class NewGame(MethodView):
    @jwt_required()
    @blp.arguments(ChessGameSchema)
    def post(self, game_data):
        game = ChessGameModel(
            user_id=get_jwt_identity(),
            puzzle_id=game_data["puzzle_id"],
            game_won=game_data["game_won"],
            game_date=game_data["game_date"],
            solving_time=game_data["solving_time"],
            user_answer=game_data["user_answer"],
        )
        db.session.add(game)
        db.session.commit()
        return {"message": "Game added successfully"}


@blp.route("/stats")
class ChessStats(MethodView):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        results = (
            db.session.query(ChessGameModel, ChessPuzzleModel)
            .join(ChessPuzzleModel, ChessGameModel.puzzle_id == ChessPuzzleModel.id)
            .filter(ChessGameModel.user_id == user_id)
            .all()
        )

        serialized_results = []
        for game, puzzle in results:
            game_data = ChessGameSchema().dump(game)
            puzzle_data = ChessPuzzleSchema().dump(puzzle)
            serialized_results.append({"game": game_data, "puzzle": puzzle_data})

        return serialized_results


@blp.route("/percentile")
class Percentile(MethodView):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        percentiles = []
        # for attribute in ["solving_time",]:

        s_rates = get_all_users_success_rates(ChessGameModel)
        print(s_rates)
        print(get_all_users_success_rates(ChessGameModel))
        success_percentile = calculate_percentile(user_id, s_rates)

        percentiles.append({"success_rate": success_percentile})

        totals = get_all_users_totals(ChessGameModel, "solving_time")
        print(totals)
        game_time_percentile = calculate_percentile(user_id, totals)
        percentiles.append({"solving_time": game_time_percentile})

        avg_ratings = (
            db.session.query(
                ChessGameModel.user_id,
                db.func.avg(ChessPuzzleModel.rating).label("avg_rating"),
            )
            .join(ChessGameModel, ChessGameModel.puzzle_id == ChessPuzzleModel.id)
            .group_by(ChessGameModel.user_id)
            .all()
        )

        avg_ratings = [(user_id, avg_rating) for user_id, avg_rating in avg_ratings]
        print(avg_ratings)
        avg_ratings.sort(key=lambda x: x[1])

        user_avg_rating = next(
            (avg_rating for uid, avg_rating in avg_ratings if uid == user_id), None
        )

        if user_avg_rating is not None:
            user_position = avg_ratings.index((user_id, user_avg_rating))
            percentile = (
                (user_position / (len(avg_ratings) - 1)) * 100
                if len(avg_ratings) > 1
                else 0
            )
            percentiles.append({"average_rating_percentile": percentile})
        else:
            percentiles.append({"average_rating_percentile": "No rating data"})

        dict_of_per = {}
        for d in percentiles:
            dict_of_per.update(d)
        return dict_of_per
