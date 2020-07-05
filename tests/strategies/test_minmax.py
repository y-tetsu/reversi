"""Tests of minmax.py
"""

import unittest

from reversi.board import BitBoard
from reversi.strategies import MinMax
from reversi.strategies.coordinator import Evaluator_T, Evaluator_TPOW


class TestMinMax(unittest.TestCase):
    """minmax
    """
    def test_minmax_init(self):
        minmax = MinMax()
        self.assertEqual(minmax._MIN, -10000000)
        self.assertEqual(minmax._MAX, 10000000)
        self.assertEqual(minmax.depth, 3)
        self.assertEqual(minmax.evaluator, None)

        minmax = MinMax(depth=4, evaluator=Evaluator_T())
        self.assertEqual(minmax._MIN, -10000000)
        self.assertEqual(minmax._MAX, 10000000)
        self.assertEqual(minmax.depth, 4)
        self.assertTrue(isinstance(minmax.evaluator, Evaluator_T))

    def test_minmax_get_score(self):
        board = BitBoard()
        minmax = MinMax(evaluator=Evaluator_T())

        self.assertEqual(minmax.get_score('black', board, 1), -3)
        self.assertEqual(minmax.get_score('black', board, 2), -1)
        self.assertEqual(minmax.get_score('black', board, 3), -4)
        self.assertEqual(minmax.get_score('black', board, 4), 0)

        board.put_disc('black', 3, 2)
        self.assertEqual(minmax.get_score('white', board, 1), -1)
        self.assertEqual(minmax.get_score('white', board, 2), -4)
        self.assertEqual(minmax.get_score('white', board, 3), 0)
        self.assertEqual(minmax.get_score('white', board, 4), -3)

    def test_minmax_next_move(self):
        board = BitBoard()
        minmax = MinMax(evaluator=Evaluator_TPOW())

        board.put_disc('black', 3, 2)
        self.assertEqual(minmax.next_move('white', board), (2, 4))

        board.put_disc('white', 2, 4)
        board.put_disc('black', 5, 5)
        board.put_disc('white', 4, 2)
        board.put_disc('black', 5, 2)
        board.put_disc('white', 5, 4)
        self.assertEqual(minmax.next_move('black', board), (2, 2))
