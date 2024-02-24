from db import db
from sqlalchemy.orm import relationship


class ChessPuzzleModel(db.Model):
    __tablename__ = "puzzles"
    id = db.Column(db.Integer, primary_key=True)
    puzzle_id = db.Column(db.String)
    fen = db.Column(db.String)
    rating = db.Column(db.Integer)
    rating_deviation = db.Column(db.Integer)
    popularity = db.Column(db.Integer)
    moves = db.Column(db.String)
    number_of_pieces = db.Column(db.Integer)
    text_position = db.Column(db.String)
    nb_plays = db.Column(db.Integer)
    themes = db.Column(db.Text)
    game_url = db.Column(db.String)
    opening_tags = db.Column(db.Text)
    chess_game = relationship("ChessGameModel", back_populates="puzzle")
