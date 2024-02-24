import chess

puzzle = dict(
    {
        "fen": "r2qr1k1/b1p2ppp/pp4n1/P1P1p3/4P1n1/B2P2Pb/3NBP1P/RN1QR1K1 b - - 1 16",
        "game_url": "https://lichess.org/4MWQCxQ6/black#Some(31)",
        "id": 4,
        "moves": "b6c5 e2g4 h3g4 d1g4",
        "nb_plays": 556,
        "opening_tags": "Kings_Pawn_Game Kings_Pawn_Game_Leonardis_Variation",
        "popularity": 87,
        "puzzle_id": "0009B",
        "rating": 1086,
        "themes": "advantage middlegame short",
    },
)


def fen_to_text(fen):
    board = chess.Board(fen)
    piece_map = board.piece_map()

    # Define the order of pieces
    piece_order = {"K": 1, "Q": 2, "R": 3, "B": 4, "N": 5, "P": 6}
    white_pieces, black_pieces = {}, {}

    for square, piece in piece_map.items():
        position = chess.square_name(square).upper()
        piece_text = (
            piece.symbol().upper()
            if piece.color == chess.WHITE
            else piece.symbol().lower()
        )
        piece_category = piece_order[piece_text.upper()]

        if piece.color == chess.WHITE:
            white_pieces.setdefault(piece_category, []).append(piece_text + position)
        else:
            black_pieces.setdefault(piece_category, []).append(piece_text + position)

    white_text = "White: " + ", ".join(
        [", ".join(white_pieces[i]) for i in sorted(white_pieces.keys()) if i != 6]
    )
    if 6 in white_pieces:
        white_text += ", P: " + ", ".join(
            pawn.replace("P", "") for pawn in white_pieces[6]
        )

    black_text = "Black: " + ", ".join(
        [", ".join(black_pieces[i]) for i in sorted(black_pieces.keys()) if i != 6]
    )
    if 6 in black_pieces:
        black_text += ", p: " + ", ".join(
            pawn.replace("p", "") for pawn in black_pieces[6]
        )
    # because of the fist move in the position is that of the opponent
    turn = "Black to play" if board.turn == chess.WHITE else "White to play"

    return f" {white_text} / {black_text} / {turn}"


def count_pieces_in_fen(fen):
    board = chess.Board(fen)
    piece_map = board.piece_map()
    return len(piece_map)


if __name__ == "__main__":
    fen_string = puzzle["fen"]  # Example FEN
    print(fen_to_text(fen_string))
