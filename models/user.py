from db import db
from sqlalchemy.orm import relationship


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    adding_games = relationship("AddingGameModel", back_populates="user")
    multiplication_games = relationship(
        "MultiplicationGameModel", back_populates="user"
    )
    chess_games = relationship("ChessGameModel", back_populates="user")
