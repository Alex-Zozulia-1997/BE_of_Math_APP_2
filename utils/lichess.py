from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import zstandard as zstd
import csv
from utils.chess_utils import count_pieces_in_fen, fen_to_text
import os
from dotenv import load_dotenv
from models import ChessPuzzleModel as Puzzle

load_dotenv()

# Replace with your actual database URL
engine = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(bind=engine)


def decompress_zst(file_path):
    with open(file_path, "rb") as compressed:
        dctx = zstd.ZstdDecompressor()
        with dctx.stream_reader(compressed) as reader:
            decompressed_data = reader.read().decode("utf-8")
    return decompressed_data


def parse_csv(data):
    lines = data.splitlines()
    reader = csv.DictReader(lines)
    parsed_data = [row for row in reader]
    return parsed_data


def insert_data_to_db(parsed_data):
    session = Session()  # Create a new session for each insert operation
    for row in parsed_data[:2000]:
        puzzle = Puzzle(
            puzzle_id=row["PuzzleId"],
            fen=row["FEN"],
            number_of_pieces=count_pieces_in_fen(row["FEN"]),
            text_position=fen_to_text(row["FEN"]),
            rating=row["Rating"],
            rating_deviation=row["RatingDeviation"],
            popularity=row["Popularity"],
            nb_plays=row["NbPlays"],
            themes=row["Themes"],
            moves=row["Moves"],
            game_url=row["GameUrl"],
            opening_tags=row["OpeningTags"],
        )
        session.add(puzzle)
    print("+1")
    session.commit()
    session.close()


file_path = "utils/lichess_db_puzzle (2).csv.zst"
decompressed_data = decompress_zst(file_path)
parsed_data = parse_csv(decompressed_data)
insert_data_to_db(parsed_data)


def drop_puzzles_table():
    session = Session()
    session.query(Puzzle).delete()
    session.commit()
    session.close()


# drop_puzzles_table()
