"""Tests of iterative.py
"""

import unittest
import os

from reversi.board import BitBoard
from reversi.strategies.common import Measure
from reversi.strategies import IterativeDeepning
from reversi.strategies.alphabeta import _AlphaBeta, AlphaBeta
import reversi.strategies.coordinator as coord


class TestIterativeDeepning(unittest.TestCase):
    """iterative
    """
    def test_iterative_init(self):
        iterative = IterativeDeepning(
            depth=2,
            selector=coord.Selector(),
            sorter=coord.Sorter_B(),
            search=AlphaBeta(
                evaluator=coord.Evaluator_TPOW(),
            )
        )

        self.assertEqual(iterative.depth, 2)
        self.assertTrue(isinstance(iterative.selector, coord.Selector))
        self.assertTrue(isinstance(iterative.sorter, coord.Sorter_B))
        self.assertTrue(isinstance(iterative.search, AlphaBeta))
        self.assertTrue(isinstance(iterative.search.evaluator, coord.Evaluator_TPOW))

    def test_iterative_next_move_depth2(self):
        board = BitBoard()

        # limit
        iterative = IterativeDeepning(
            depth=2,
            selector=coord.Selector(),
            sorter=coord.Sorter_B(),
            search=_AlphaBeta(
                evaluator=coord.Evaluator_TPOW(),
            ),
            limit=4,
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
        self.assertGreaterEqual(iterative.max_depth, 4)

        # performance
        iterative = IterativeDeepning(
            depth=2,
            selector=coord.Selector(),
            sorter=coord.Sorter_B(),
            search=AlphaBeta(
                evaluator=coord.Evaluator_TPOW(),
            ),
        )

        key = iterative.__class__.__name__ + str(os.getpid())
        Measure.elp_time[key] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}
        key2 = iterative.search.__class__.__name__ + str(os.getpid())
        Measure.count[key2] = 0
        iterative.next_move('black', board)

        print()
        print(key)
        print(' min :', Measure.elp_time[key]['min'], '(s)')
        print(' max :', Measure.elp_time[key]['max'], '(s)')
        print(' ave :', Measure.elp_time[key]['ave'], '(s)')
        print('(3500)', Measure.count[key2])
        print('(max_depth=5)', iterative.max_depth)
