"""Tests of alphabeta.py
"""

import unittest
import os
import time

from reversi.board import BitBoard
from reversi.strategies import _AlphaBeta, AlphaBeta
from reversi.strategies.coordinator import Evaluator_T, Evaluator_TPW, Evaluator_TPOW
from reversi.strategies.common import Timer, Measure, CPU_TIME
from reversi.strategies.coordinator import Sorter_B


class TestAlphaBeta(unittest.TestCase):
    """alphabeta
    """
    def test_alphabeta_init(self):
        alphabeta = _AlphaBeta()
        self.assertEqual(alphabeta._MIN, -10000000)
        self.assertEqual(alphabeta._MAX, 10000000)
        self.assertEqual(alphabeta.depth, 3)
        self.assertEqual(alphabeta.evaluator, None)

        alphabeta = _AlphaBeta(depth=4, evaluator=Evaluator_T())
        self.assertEqual(alphabeta._MIN, -10000000)
        self.assertEqual(alphabeta._MAX, 10000000)
        self.assertEqual(alphabeta.depth, 4)
        self.assertTrue(isinstance(alphabeta.evaluator, Evaluator_T))

        alphabeta = AlphaBeta()
        self.assertEqual(alphabeta._MIN, -10000000)
        self.assertEqual(alphabeta._MAX, 10000000)
        self.assertEqual(alphabeta.depth, 3)
        self.assertEqual(alphabeta.evaluator, None)

        alphabeta = AlphaBeta(depth=4, evaluator=Evaluator_T())
        self.assertEqual(alphabeta._MIN, -10000000)
        self.assertEqual(alphabeta._MAX, 10000000)
        self.assertEqual(alphabeta.depth, 4)
        self.assertTrue(isinstance(alphabeta.evaluator, Evaluator_T))

    def test_alphabeta_get_score(self):
        board = BitBoard()
        alphabeta = _AlphaBeta(evaluator=Evaluator_T())
        self.assertEqual(alphabeta._get_score('black', board, alphabeta._MIN, alphabeta._MAX, 1), -3)
        self.assertEqual(alphabeta._get_score('black', board, alphabeta._MIN, alphabeta._MAX, 2), -1)
        self.assertEqual(alphabeta._get_score('black', board, alphabeta._MIN, alphabeta._MAX, 3), -4)
        self.assertEqual(alphabeta._get_score('black', board, alphabeta._MIN, alphabeta._MAX, 4), 0)

        board.put_disc('black', 3, 2)
        self.assertEqual(alphabeta._get_score('white', board, alphabeta._MIN, alphabeta._MAX, 1), 1)
        self.assertEqual(alphabeta._get_score('white', board, alphabeta._MIN, alphabeta._MAX, 2), 4)
        self.assertEqual(alphabeta._get_score('white', board, alphabeta._MIN, alphabeta._MAX, 3), 0)
        self.assertEqual(alphabeta._get_score('white', board, alphabeta._MIN, alphabeta._MAX, 4), 3)

    def test_alphabeta_next_move(self):
        board = BitBoard()
        alphabeta = _AlphaBeta(evaluator=Evaluator_TPOW())

        board.put_disc('black', 3, 2)
        self.assertEqual(alphabeta.next_move('white', board), (2, 4))

        board.put_disc('white', 2, 4)
        board.put_disc('black', 5, 5)
        board.put_disc('white', 4, 2)
        board.put_disc('black', 5, 2)
        board.put_disc('white', 5, 4)
        self.assertEqual(alphabeta.next_move('black', board), (2, 2))

    def test_alphabeta_get_best_move(self):
        board = BitBoard()
        alphabeta = _AlphaBeta(evaluator=Evaluator_TPW())

        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 4)
        board.put_disc('black', 5, 5)
        board.put_disc('white', 4, 2)
        board.put_disc('black', 5, 2)
        board.put_disc('white', 5, 4)
        moves = board.get_legal_moves('black').keys()
        self.assertEqual(alphabeta.get_best_move('black', board, moves, 5), ((2, 2), {(2, 2): 8, (2, 3): 8, (5, 3): 8, (1, 5): 8, (2, 5): 8, (3, 5): 8, (4, 5): 8, (6, 5): 8}))  # noqa: E501

    def test_alphabeta_performance_of_get_score(self):
        board = BitBoard()
        board.put_disc('black', 3, 2)

        # AlphaBeta
        alphabeta = AlphaBeta(evaluator=Evaluator_TPOW())
        key = alphabeta.__class__.__name__ + str(os.getpid())

        Measure.count[key] = 0
        Timer.timeout_flag[key] = False
        Timer.timeout_value[key] = 0
        Timer.deadline[key] = time.time() + CPU_TIME
        score = alphabeta._get_score('white', board, alphabeta._MIN, alphabeta._MAX, 5)  # depth 5
        self.assertEqual(score, 4)
        self.assertEqual(Measure.count[key], 703)

        # _AlphaBeta
        alphabeta = _AlphaBeta(evaluator=Evaluator_TPOW())
        key = alphabeta.__class__.__name__ + str(os.getpid())

        Measure.count[key] = 0
        score = alphabeta._get_score('white', board, alphabeta._MIN, alphabeta._MAX, 2)  # depth 2
        self.assertEqual(score, -10.75)
        self.assertEqual(Measure.count[key], 16)

        Measure.count[key] = 0
        score = alphabeta._get_score('white', board, alphabeta._MIN, alphabeta._MAX, 3)  # depth 3
        self.assertEqual(score, 6.25)
        self.assertEqual(Measure.count[key], 63)

        Measure.count[key] = 0
        score = alphabeta._get_score('white', board, alphabeta._MIN, alphabeta._MAX, 4)  # depth 4
        self.assertEqual(score, -8.25)
        self.assertEqual(Measure.count[key], 257)

        Measure.count[key] = 0
        score = alphabeta._get_score('white', board, alphabeta._MIN, alphabeta._MAX, 5)  # depth 5
        self.assertEqual(score, 4)
        self.assertEqual(Measure.count[key], 703)

        Measure.count[key] = 0
        score = alphabeta._get_score('white', board, alphabeta._MIN, alphabeta._MAX, 6)  # depth 6
        self.assertEqual(score, -3.5)
        self.assertEqual(Measure.count[key], 2696)

        board.put_disc('white', 2, 4)
        board.put_disc('black', 5, 5)
        board.put_disc('white', 4, 2)
        board.put_disc('black', 5, 2)
        board.put_disc('white', 5, 4)
        Measure.elp_time[key] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}
        for _ in range(5):
            alphabeta.next_move('black', board)

        print()
        print(key, 'depth = 3')
        print(' min :', Measure.elp_time[key]['min'], '(s)')
        print(' max :', Measure.elp_time[key]['max'], '(s)')
        print(' ave :', Measure.elp_time[key]['ave'], '(s)')

        # best move
        class _AlphaBetaTest(_AlphaBeta):
            @Measure.time
            def get_best_move(self, color, board, moves, depth):
                return super().get_best_move(color, board, moves, depth)

        alphabeta = _AlphaBetaTest(evaluator=Evaluator_TPOW())
        key = alphabeta.__class__.__name__ + str(os.getpid())

        moves = list(board.get_legal_moves('black').keys())
        Measure.elp_time[key] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}
        for _ in range(3):
            alphabeta.get_best_move('black', board, moves, 4)

        print()
        print(key, 'depth = 4')
        print(' min :', Measure.elp_time[key]['min'], '(s)')
        print(' max :', Measure.elp_time[key]['max'], '(s)')
        print(' ave :', Measure.elp_time[key]['ave'], '(s)')
        self.assertEqual(alphabeta.get_best_move('black', board, moves, 4), ((5, 3), {(2, 2): -4.25, (2, 3): -3.75, (5, 3): -1.75, (1, 5): -1.75, (2, 5): -1.75, (3, 5): -1.75, (4, 5): -1.75, (6, 5): -1.75}))  # noqa: E501

        moves = Sorter_B().sort_moves(color='black', board=board, moves=moves, best_move=(5, 3))
        Measure.elp_time[key] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}
        for _ in range(3):
            alphabeta.get_best_move('black', board, moves, 4)

        print()
        print(key, 'depth = 4 Sorter_B')
        print(' min :', Measure.elp_time[key]['min'], '(s)')
        print(' max :', Measure.elp_time[key]['max'], '(s)')
        print(' ave :', Measure.elp_time[key]['ave'], '(s)')

    def test_alphabeta_timer_timeout(self):
        board = BitBoard()
        board.put_disc('black', 3, 2)
        alphabeta = AlphaBeta(depth=10, evaluator=Evaluator_TPOW())
        key = alphabeta.__class__.__name__ + str(os.getpid())
        Measure.elp_time[key] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}
        Measure.count[key] = 0

        alphabeta.next_move('white', board)
        self.assertTrue(Timer.timeout_flag[key])
        self.assertLessEqual(Measure.elp_time[key]['max'], CPU_TIME * 1.1)
        print('(2600)', Measure.count[key])
