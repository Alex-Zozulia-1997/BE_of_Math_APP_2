import unittest
from utils.chess_utils import (
    fen_to_text,
)


class TestFenToText(unittest.TestCase):
    def test_fen_to_text(self):
        fen = "r2qr1k1/b1p2ppp/pp4n1/P1P1p3/4P1n1/B2P2Pb/3NBP1P/RN1QR1K1 b - - 1 16"
        expected_output = "White: KG1, QD1, RE1, RA1, BA3, BE2, ND2, NB1, P: C5, A5, E4, G3, D3, H2, F2 / Black: kG8, qD8, rE8, rA8, bA7, bH3, nG6, nG4, p: H7, G7, F7, C7, B6, A6, E5 / White to play"
        self.assertEqual(fen_to_text(fen).strip(), expected_output)


if __name__ == "__main__":
    unittest.main()
