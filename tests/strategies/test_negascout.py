"""Tests of negascout.py
"""

import unittest
import os
import time

from reversi.board import BitBoard
from reversi.strategies.common import Timer, Measure, CPU_TIME
from reversi.strategies import _NegaScout, NegaScout
import reversi.strategies.coordinator as coord


class TestNegaScout(unittest.TestCase):
    """negascout
    """
    def test_negascout_init(self):
        negascout = _NegaScout()
        self.assertEqual(negascout._MIN, -10000000)
        self.assertEqual(negascout._MAX, 10000000)
        self.assertEqual(negascout.depth, 3)
        self.assertEqual(negascout.evaluator, None)

        negascout = _NegaScout(depth=4, evaluator=coord.Evaluator_T())
        self.assertEqual(negascout._MIN, -10000000)
        self.assertEqual(negascout._MAX, 10000000)
        self.assertEqual(negascout.depth, 4)
        self.assertTrue(isinstance(negascout.evaluator, coord.Evaluator_T))

        negascout = NegaScout()
        self.assertEqual(negascout._MIN, -10000000)
        self.assertEqual(negascout._MAX, 10000000)
        self.assertEqual(negascout.depth, 3)
        self.assertEqual(negascout.evaluator, None)

        negascout = NegaScout(depth=4, evaluator=coord.Evaluator_T())
        self.assertEqual(negascout._MIN, -10000000)
        self.assertEqual(negascout._MAX, 10000000)
        self.assertEqual(negascout.depth, 4)
        self.assertTrue(isinstance(negascout.evaluator, coord.Evaluator_T))

    def test_negascout_get_score(self):
        board = BitBoard()
        negascout = _NegaScout(evaluator=coord.Evaluator_T())
        self.assertEqual(negascout._get_score('black', board, negascout._MIN, negascout._MAX, 1), -3)
        self.assertEqual(negascout._get_score('black', board, negascout._MIN, negascout._MAX, 2), -1)
        self.assertEqual(negascout._get_score('black', board, negascout._MIN, negascout._MAX, 3), -4)
        self.assertEqual(negascout._get_score('black', board, negascout._MIN, negascout._MAX, 4), 0)

        board.put_disc('black', 3, 2)
        self.assertEqual(negascout._get_score('white', board, negascout._MIN, negascout._MAX, 1), 1)
        self.assertEqual(negascout._get_score('white', board, negascout._MIN, negascout._MAX, 2), 4)
        self.assertEqual(negascout._get_score('white', board, negascout._MIN, negascout._MAX, 3), 0)
        self.assertEqual(negascout._get_score('white', board, negascout._MIN, negascout._MAX, 4), 3)

    def test_negascout_next_move(self):
        board = BitBoard()
        negascout = _NegaScout(evaluator=coord.Evaluator_TPOW())

        board.put_disc('black', 3, 2)
        self.assertEqual(negascout.next_move('white', board), (2, 4))

        board.put_disc('white', 2, 4)
        board.put_disc('black', 5, 5)
        board.put_disc('white', 4, 2)
        board.put_disc('black', 5, 2)
        board.put_disc('white', 5, 4)
        self.assertEqual(negascout.next_move('black', board), (2, 2))

    def test_negascout_get_best_move(self):
        board = BitBoard()
        negascout = _NegaScout(evaluator=coord.Evaluator_TPW())

        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 4)
        board.put_disc('black', 5, 5)
        board.put_disc('white', 4, 2)
        board.put_disc('black', 5, 2)
        board.put_disc('white', 5, 4)
        moves = board.get_legal_moves('black')
        self.assertEqual(negascout.get_best_move('black', board, moves, 5), ((2, 2), {(2, 2): 8, (2, 3): 8, (5, 3): 8, (1, 5): 8, (2, 5): 8, (3, 5): 8, (4, 5): 8, (6, 5): 8}))  # noqa: E501

    def test_negascout_performance_of_get_score(self):
        board = BitBoard()
        board.put_disc('black', 3, 2)

        # NegaScout
        negascout = NegaScout(evaluator=coord.Evaluator_TPOW())
        key = negascout.__class__.__name__ + str(os.getpid())

        Measure.count[key] = 0
        Timer.timeout_flag[key] = False
        Timer.timeout_value[key] = 0
        Timer.deadline[key] = time.time() + CPU_TIME
        score = negascout._get_score('white', board, negascout._MIN, negascout._MAX, 5)  # depth 5
        self.assertEqual(score, 4)
        self.assertEqual(Measure.count[key], 568)

        # _NegaScout
        negascout = _NegaScout(evaluator=coord.Evaluator_TPOW())
        key = negascout.__class__.__name__ + str(os.getpid())

        Measure.count[key] = 0
        score = negascout._get_score('white', board, negascout._MIN, negascout._MAX, 2)  # depth 2
        self.assertEqual(score, -10.75)
        self.assertEqual(Measure.count[key], 22)

        Measure.count[key] = 0
        score = negascout._get_score('white', board, negascout._MIN, negascout._MAX, 3)  # depth 3
        self.assertEqual(score, 6.25)
        self.assertEqual(Measure.count[key], 116)

        Measure.count[key] = 0
        score = negascout._get_score('white', board, negascout._MIN, negascout._MAX, 4)  # depth 4
        self.assertEqual(score, -8.25)
        self.assertEqual(Measure.count[key], 516)

        Measure.count[key] = 0
        score = negascout._get_score('white', board, negascout._MIN, negascout._MAX, 5)  # depth 5
        self.assertEqual(score, 4)
        self.assertEqual(Measure.count[key], 568)

        Measure.count[key] = 0
        score = negascout._get_score('white', board, negascout._MIN, negascout._MAX, 6)  # depth 6
        self.assertEqual(score, -3.5)
        self.assertEqual(Measure.count[key], 2449)

        board.put_disc('white', 2, 4)
        board.put_disc('black', 5, 5)
        board.put_disc('white', 4, 2)
        board.put_disc('black', 5, 2)
        board.put_disc('white', 5, 4)
        Measure.elp_time[key] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}
        for _ in range(5):
            negascout.next_move('black', board)

        print()
        print(key, 'depth = 3')
        print(' min :', Measure.elp_time[key]['min'], '(s)')
        print(' max :', Measure.elp_time[key]['max'], '(s)')
        print(' ave :', Measure.elp_time[key]['ave'], '(s)')

        # best move
        class _NegaScoutTest(_NegaScout):
            @Measure.time
            def get_best_move(self, color, board, moves, depth):
                return super().get_best_move(color, board, moves, depth)

        negascout = _NegaScoutTest(evaluator=coord.Evaluator_TPOW())
        key = negascout.__class__.__name__ + str(os.getpid())

        moves = board.get_legal_moves('black')
        Measure.elp_time[key] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}
        for _ in range(3):
            negascout.get_best_move('black', board, moves, 4)

        print()
        print(key, 'depth = 4')
        print(' min :', Measure.elp_time[key]['min'], '(s)')
        print(' max :', Measure.elp_time[key]['max'], '(s)')
        print(' ave :', Measure.elp_time[key]['ave'], '(s)')
        self.assertEqual(negascout.get_best_move('black', board, moves, 4), ((5, 3), {(2, 2): -4.25, (2, 3): -3.75, (5, 3): -1.75, (1, 5): -1.75, (2, 5): -1.75, (3, 5): -1.75, (4, 5): -1.75, (6, 5): -1.75}))  # noqa: E501

        moves = coord.Sorter_B().sort_moves(color='black', board=board, moves=moves, best_move=(5, 3))
        Measure.elp_time[key] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}
        for _ in range(3):
            negascout.get_best_move('black', board, moves, 4)

        print()
        print(key, 'depth = 4 Sorter_B')
        print(' min :', Measure.elp_time[key]['min'], '(s)')
        print(' max :', Measure.elp_time[key]['max'], '(s)')
        print(' ave :', Measure.elp_time[key]['ave'], '(s)')

    def test_negascout_timer_timeout(self):
        board = BitBoard()
        board.put_disc('black', 3, 2)
        negascout = NegaScout(depth=10, evaluator=coord.Evaluator_TPOW())
        key = negascout.__class__.__name__ + str(os.getpid())
        Measure.elp_time[key] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}
        Measure.count[key] = 0

        negascout.next_move('white', board)
        self.assertTrue(Timer.timeout_flag[key])
        self.assertLessEqual(Measure.elp_time[key]['max'], CPU_TIME * 1.1)
        print('(4000)', Measure.count[key])
