"""Tests of joseki.py
"""

import unittest

from reversi.board import BitBoard
from reversi.strategies import AbstractStrategy, Random, _Joseki_


class TestJoseki(unittest.TestCase):
    """joseki
    """
    def test_joseki_init(self):
        joseki = _Joseki_(Random())

        self.assertEqual(joseki.joseki, {})
        self.assertIsInstance(joseki.base, Random)

    def test_joseki_next_move(self):
        class Origin(AbstractStrategy):
            def next_move(self, color, board):
                return (0, 0)

        joseki = _Joseki_(Origin())
        board = BitBoard(4)
        self.assertEqual(joseki.next_move('black', board), (0, 0))

        board = BitBoard(8)
        self.assertEqual(joseki.next_move('black', board), (0, 0))

        joseki.joseki = {
            ('black', 0x0000000810000000, 0x0000001008000000): (5, 4),
        }
        self.assertEqual(joseki.next_move('black', board), (5, 4))
