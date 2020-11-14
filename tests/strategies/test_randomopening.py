"""Tests of randomopening.py
"""

import unittest

from reversi.board import Board
from reversi.strategies import RandomOpening
from reversi.strategies.easy import Random


class TestRandomOpening(unittest.TestCase):
    """randomopening
    """
    def test_randomopening_init(self):
        class TestStrategy:
            pass

        randomopening = RandomOpening(depth=2, base=TestStrategy())
        self.assertEqual(randomopening.depth, 2)
        self.assertTrue(isinstance(randomopening.random, Random))
        self.assertTrue(isinstance(randomopening.base, TestStrategy))

    def test_randomopening_next_move(self):
        class TestStrategy:
            def next_move(self, color, board):
                return (0, 0)

        board = Board()
        randomopening = RandomOpening(depth=4, base=TestStrategy())

        # depth = 1 - 4
        for _ in range(2):
            for color in ('black', 'white'):
                move = randomopening.next_move(color, board)
                self.assertNotEqual(move, (0, 0))
                board.put_disc(color, *move)

        # depth = 5
        move = randomopening.next_move('black', board)
        self.assertEqual(move, (0, 0))
