"""Tests of iterative.py
"""

import unittest
import os

from reversi.board import BitBoard
from reversi.strategies import IterativeDeepning
from reversi.strategies.alphabeta import AlphaBeta
from reversi.strategies.coordinator import Evaluator_TPOW, Selector, Sorter_B
from reversi.strategies.common import Measure


class TestIterativeDeepning(unittest.TestCase):
    """iterative
    """
    def test_iterative_init(self):
        iterative = IterativeDeepning(
            depth=2,
            selector=Selector(),
            sorter=Sorter_B(),
            search=AlphaBeta(
                evaluator=Evaluator_TPOW(),
            )
        )

        self.assertEqual(iterative.depth, 2)
        self.assertTrue(isinstance(iterative.selector, Selector))
        self.assertTrue(isinstance(iterative.sorter, Sorter_B))
        self.assertTrue(isinstance(iterative.search, AlphaBeta))
        self.assertTrue(isinstance(iterative.search.evaluator, Evaluator_TPOW))

    def test_iterative_next_move_depth2(self):
        board = BitBoard()
        iterative = IterativeDeepning(
            depth=2,
            selector=Selector(),
            sorter=Sorter_B(),
            search=AlphaBeta(
                evaluator=Evaluator_TPOW(),
            )
        )

        key = iterative.__class__.__name__ + str(os.getpid())
        Measure.elp_time[key] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}
        key2 = iterative.search.__class__.__name__ + str(os.getpid())
        Measure.count[key2] = 0

        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 4)
        board.put_disc('black', 5, 5)
        board.put_disc('white', 4, 2)
        board.put_disc('black', 5, 2)
        board.put_disc('white', 5, 4)
        self.assertEqual(iterative.next_move('black', board), (5, 3))
        self.assertGreaterEqual(iterative.max_depth, 5)

        print()
        print(key, 'remain = 9')
        print(' min :', Measure.elp_time[key]['min'], '(s)')
        print(' max :', Measure.elp_time[key]['max'], '(s)')
        print(' ave :', Measure.elp_time[key]['ave'], '(s)')
        print('(2000)', Measure.count[key2])
