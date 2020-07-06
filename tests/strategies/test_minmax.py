"""Tests of minmax.py
"""

import unittest
import os

from reversi.board import BitBoard
from reversi.strategies import MinMax
from reversi.strategies.coordinator import Evaluator_T, Evaluator_TPOW
from reversi.strategies.common import Timer, Measure, CPU_TIME


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

    def test_minmax_performance_of_get_score(self):
        board = BitBoard()
        board.put_disc('black', 3, 2)

        minmax = MinMax(evaluator=Evaluator_TPOW())
        key = minmax.__class__.__name__ + str(os.getpid())

        Measure.count[key] = 0
        score = minmax.get_score('white', board, 2)  # depth 2
        self.assertEqual(score, 10.75)
        self.assertEqual(Measure.count[key], 18)

        Measure.count[key] = 0
        score = minmax.get_score('white', board, 3)  # depth 3
        self.assertEqual(score, -6.25)
        self.assertEqual(Measure.count[key], 79)

        Measure.count[key] = 0
        score = minmax.get_score('white', board, 4)  # depth 4
        self.assertEqual(score, 8.25)
        self.assertEqual(Measure.count[key], 428)

        Measure.count[key] = 0
        score = minmax.get_score('white', board, 5)  # depth 5
        self.assertEqual(score, -4)
        self.assertEqual(Measure.count[key], 2478)

        board.put_disc('white', 2, 4)
        board.put_disc('black', 5, 5)
        board.put_disc('white', 4, 2)
        board.put_disc('black', 5, 2)
        board.put_disc('white', 5, 4)
        Measure.elp_time[key] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}
        for _ in range(5):
            minmax.next_move('white', board)

        print()
        print(key)
        print(' min :', Measure.elp_time[key]['min'], '(s)')
        print(' max :', Measure.elp_time[key]['max'], '(s)')
        print(' ave :', Measure.elp_time[key]['ave'], '(s)')
