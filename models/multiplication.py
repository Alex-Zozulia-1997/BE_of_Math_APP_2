from db import db
from sqlalchemy.orm import relationship


class MultiplicationGameModel(db.Model):
    __tablename__ = "multiplication_game"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    game_won = db.Column(db.Boolean, nullable=False)
    game_date = db.Column(db.DateTime, nullable=False)
    total_number_of_digits = db.Column(db.Integer, nullable=False)
    multiplication_time = db.Column(db.Integer, nullable=False)
    user_answer = db.Column(db.Integer, nullable=False)
    correct_answer = db.Column(db.Integer, nullable=False)
    user = relationship("UserModel", back_populates="multiplication_games")
