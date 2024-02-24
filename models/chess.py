from db import db
from sqlalchemy.orm import relationship


class ChessGameModel(db.Model):
    __tablename__ = "chess_game"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    puzzle_id = db.Column(db.Integer, db.ForeignKey("puzzles.id"), nullable=False)
    game_won = db.Column(db.Boolean, nullable=False)
    solving_time = db.Column(db.Integer, nullable=False)
    game_date = db.Column(db.DateTime, nullable=False)
    user_answer = db.Column(db.String, nullable=False)
    user = relationship("UserModel", back_populates="chess_games")
    puzzle = relationship("ChessPuzzleModel", back_populates="chess_game")
