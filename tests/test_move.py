"""Tests of move.py
"""

import unittest

from reversi import Move as m
from reversi.move import M, LOWER
from reversi.board import Board


class TestMove(unittest.TestCase):
    """move
    """
    def test_new(self):
        # objects are work as tuple
        self.assertEqual(m(0, 0), (0, 0))
        self.assertEqual(m(7, 7), (7, 7))
        self.assertEqual(m('c8'), (2, 7))
        self.assertEqual(m('Z8'), (25, 7))

    def test_init(self):
        # none
        patterns = [m(), M]
        for pattern in patterns:
            self.assertIsNone(pattern._Move__x)
            self.assertIsNone(pattern._Move__y)
            self.assertEqual(pattern._Move__str, '')
            self.assertEqual(pattern._Move__case, LOWER)

        # x, y, str
        patterns = [m(0, 1), m('a2')]
        for pattern in patterns:
            self.assertEqual(pattern._Move__x, 0)
            self.assertEqual(pattern._Move__y, 1)
            self.assertEqual(pattern._Move__str, 'a2')

        # case
        move = m(case='upper')
        self.assertEqual(move._Move__case, 'upper')
        move = m(case='LOWER')
        self.assertEqual(move._Move__case, LOWER)

        # put_disc
        board = Board()
        board.put_disc('black', *m('f5'))
        self.assertEqual(board.get_bitboard_info(), (34829500416, 68719476736, 0))
        board.put_disc('white', *m('d6'))
        self.assertEqual(board.get_bitboard_info(), (34561064960, 68988960768, 0))

    def test_iter(self):
        x, y = m(0, 1)
        self.assertEqual((x, y), (0, 1))

        x, y = m('a2')
        self.assertEqual((x, y), (0, 1))

    def test_repr(self):
        self.assertEqual(repr(m()), 'Move(None, None) ""')
        self.assertEqual(repr(m(1, 2)), 'Move(1, 2) "b3"')
        self.assertEqual(repr(m('b3')), 'Move(1, 2) "b3"')
        self.assertEqual(repr(m(7, 8, case='upper')), 'Move(7, 8) "H9"')
        self.assertEqual(repr(m('H9', case='upper')), 'Move(7, 8) "H9"')

    def test_str(self):
        self.assertEqual(str(m()), '')
        self.assertEqual(str(m(1, 2)), 'b3')
        self.assertEqual(str(m('b3')), 'b3')
        self.assertEqual(str(m(7, 8, case='upper')), 'H9')
        self.assertEqual(str(m('H9', case='upper')), 'H9')

    def test_get_xy(self):
        self.assertEqual(m._get_xy(), (None, None))
        self.assertEqual(m._get_xy(3, 5), (3, 5))
        self.assertEqual(m._get_xy('K15'), (10, 14))

    def test_to_xy(self):
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
            self.assertEqual(M.to_xy(pattern), expected)

        board = Board()
        board.put_disc('black', *M.to_xy('f5'))
        self.assertEqual(board.get_bitboard_info(), (34829500416, 68719476736, 0))
        board.put_disc('white', *M.to_xy('d6'))
        self.assertEqual(board.get_bitboard_info(), (34561064960, 68988960768, 0))

    def test_to_str(self):
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
            self.assertEqual(M.to_str(x, y), expected)
        # upper
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
            self.assertEqual(M.to_str(x, y, case='upper'), expected)
