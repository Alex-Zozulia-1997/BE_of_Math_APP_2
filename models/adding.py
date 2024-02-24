from db import db
from sqlalchemy.orm import relationship


class AddingGameModel(db.Model):
    __tablename__ = "adding_game"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    game_won = db.Column(db.Boolean, nullable=False)
    game_time = db.Column(db.Integer, nullable=False)
    game_date = db.Column(db.DateTime, nullable=False)
    number_of_digits = db.Column(db.Integer, nullable=False)
    seconds = db.Column(db.Integer, nullable=False)
    actions = db.Column(db.Integer, nullable=False)
    user_answer = db.Column(db.Integer, nullable=False)
    correct_answer = db.Column(db.Integer, nullable=False)
    user = relationship("UserModel", back_populates="adding_games")
