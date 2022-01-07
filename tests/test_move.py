"""Tests of move.py
"""

import unittest

from reversi.move import Move, M, LOWER
from reversi.board import Board


class TestMove(unittest.TestCase):
    """move
    """
    def test_move_init(self):
        patterns = [Move(), M]
        for pattern in patterns:
            self.assertEqual(pattern.case, LOWER)

    def test_to_xy_ok(self):
        m = Move()
        patterns = [
            ('a1', (0, 0)),
            ('A1', (0, 0)),  # upper case is also ok.
            ('a2', (0, 1)),
            ('a8', (0, 7)),
            ('b1', (1, 0)),
            ('b2', (1, 1)),
            ('h1', (7, 0)),
            ('h8', (7, 7)),
            ('z1', (25, 0)),
            ('a26', (0, 25)),
            ('z26', (25, 25)),
        ]
        for pattern, expected in patterns:
            self.assertEqual(m.to_xy(pattern), expected)

        board = Board()
        board.put_disc('black', *m.to_xy('f5'))
        self.assertEqual(board.get_bitboard_info(), (34829500416, 68719476736))
        board.put_disc('white', *m.to_xy('d6'))
        self.assertEqual(board.get_bitboard_info(), (34561064960, 68988960768))

    def test_to_str_ok(self):
        m = Move()
        # lower
        patterns = [
            (0, 0, 'a1'),
            (0, 1, 'a2'),
            (0, 7, 'a8'),
            (1, 0, 'b1'),
            (1, 1, 'b2'),
            (7, 0, 'h1'),
            (7, 7, 'h8'),
            (25, 0, 'z1'),
            (0, 25, 'a26'),
            (25, 25, 'z26'),
        ]
        for x, y, expected in patterns:
            self.assertEqual(m.to_str(x, y), expected)
        # upper
        m.case = 'upper'
        patterns = [
            (0, 0, 'A1'),
            (0, 1, 'A2'),
            (0, 7, 'A8'),
            (1, 0, 'B1'),
            (1, 1, 'B2'),
            (7, 0, 'H1'),
            (7, 7, 'H8'),
            (25, 0, 'Z1'),
            (0, 25, 'A26'),
            (25, 25, 'Z26'),
        ]
        for x, y, expected in patterns:
            self.assertEqual(m.to_str(x, y), expected)
