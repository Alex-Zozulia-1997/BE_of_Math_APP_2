from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class AddingGameSchema(Schema):
    user_id = fields.Int(required=True)
    game_won = fields.Bool(required=True)
    game_time = fields.Int(required=True)
    game_date = fields.DateTime(required=True)
    number_of_digits = fields.Int(required=True)
    seconds = fields.Int(required=True)
    actions = fields.Int(required=True)
    user_answer = fields.Int(required=True)
    correct_answer = fields.Int(required=True)


class MuiltplyGameSchema(Schema):
    user_id = fields.Int(required=True)
    game_won = fields.Bool(required=True)
    game_date = fields.DateTime(required=True)
    total_number_of_digits = fields.Int(required=True)
    multiplication_time = fields.Int(required=True)
    user_answer = fields.Int(required=True)
    correct_answer = fields.Int(required=True)


class ChessGameSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    puzzle_id = fields.Int(required=True)
    game_won = fields.Bool(required=True)
    game_date = fields.DateTime(required=True)
    solving_time = fields.Int(required=True)
    user_answer = fields.Str(required=True)


class ChessPuzzleSchema(Schema):
    id = fields.Int(required=True)
    puzzle_id = fields.Str(required=True)
    fen = fields.Str(required=True)
    moves = fields.Str(required=True)
    number_of_pieces = fields.Int(required=True)
    text_position = fields.Str(required=True)
    rating = fields.Int(required=True)
    ratingDeviation = fields.Int(required=False)
    popularity = fields.Int(required=False)
    nb_plays = fields.Int(required=False)
    themes = fields.Str(required=False)
    game_url = fields.Str(required=False)
    opening_tags = fields.Str(required=False)
