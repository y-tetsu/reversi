"""Tests of negamax.py
"""

import unittest
import os
import time

from reversi.board import BitBoard
from reversi.strategies.common import Timer, Measure, CPU_TIME
from reversi.strategies import _NegaMax_, _NegaMax, NegaMax_, NegaMax
import reversi.strategies.coordinator as coord


class TestNegaMax(unittest.TestCase):
    """negamax
    """
    def test_negamax_init(self):
        for instance in [_NegaMax_, _NegaMax, NegaMax_, NegaMax]:
            negamax = instance()
            self.assertEqual(negamax._MIN, -10000000)
            self.assertEqual(negamax.depth, 3)
            self.assertEqual(negamax.evaluator, None)

            negamax = instance(depth=4, evaluator=coord.Evaluator_T())
            self.assertEqual(negamax._MIN, -10000000)
            self.assertEqual(negamax.depth, 4)
            self.assertTrue(isinstance(negamax.evaluator, coord.Evaluator_T))

    def test_negamax_get_score(self):
        for instance in [_NegaMax_, _NegaMax, NegaMax_, NegaMax]:
            board = BitBoard()
            negamax = instance(evaluator=coord.Evaluator_T())

            self.assertEqual(negamax.get_score('black', board, 1), -3)
            self.assertEqual(negamax.get_score('black', board, 2), -1)
            self.assertEqual(negamax.get_score('black', board, 3), -4)
            self.assertEqual(negamax.get_score('black', board, 4), 0)

            board.put_disc('black', 3, 2)
            self.assertEqual(negamax.get_score('white', board, 1), 1)
            self.assertEqual(negamax.get_score('white', board, 2), 4)
            self.assertEqual(negamax.get_score('white', board, 3), 0)
            self.assertEqual(negamax.get_score('white', board, 4), 3)

    def test_negamax_next_move(self):
        for instance in [_NegaMax_, _NegaMax, NegaMax_, NegaMax]:
            board = BitBoard()
            negamax = instance(evaluator=coord.Evaluator_TPOW())

            board.put_disc('black', 3, 2)
            self.assertEqual(negamax.next_move('white', board), (2, 4))

            board.put_disc('white', 2, 4)
            board.put_disc('black', 5, 5)
            board.put_disc('white', 4, 2)
            board.put_disc('black', 5, 2)
            board.put_disc('white', 5, 4)
            self.assertEqual(negamax.next_move('black', board), (2, 2))

    def test_negamax_performance_of_get_score(self):
        board = BitBoard()
        board.put_disc('black', 3, 2)

        # NegaMax
        negamax = NegaMax(evaluator=coord.Evaluator_TPOW())
        pid = negamax.__class__.__name__ + str(os.getpid())

        Measure.count[pid] = 0
        Timer.timeout_flag[pid] = False
        Timer.timeout_value[pid] = 0
        Timer.deadline[pid] = time.time() + CPU_TIME
        score = negamax.get_score('white', board, 4, pid=pid)  # depth 4
        self.assertEqual(score, -8.25)
        self.assertEqual(Measure.count[pid], 428)

        # _NegaMax
        negamax = _NegaMax(evaluator=coord.Evaluator_TPOW())
        pid = negamax.__class__.__name__ + str(os.getpid())

        Measure.count[pid] = 0
        score = negamax.get_score('white', board, 2, pid=pid)  # depth 2
        self.assertEqual(score, -10.75)
        self.assertEqual(Measure.count[pid], 18)

        Measure.count[pid] = 0
        score = negamax.get_score('white', board, 3, pid=pid)  # depth 3
        self.assertEqual(score, 6.25)
        self.assertEqual(Measure.count[pid], 79)

        Measure.count[pid] = 0
        score = negamax.get_score('white', board, 4, pid=pid)  # depth 4
        self.assertEqual(score, -8.25)
        self.assertEqual(Measure.count[pid], 428)

        Measure.count[pid] = 0
        score = negamax.get_score('white', board, 5, pid=pid)  # depth 5
        self.assertEqual(score, 4)
        self.assertEqual(Measure.count[pid], 2478)

        board.put_disc('white', 2, 4)
        board.put_disc('black', 5, 5)
        board.put_disc('white', 4, 2)
        board.put_disc('black', 5, 2)
        board.put_disc('white', 5, 4)
        Measure.elp_time[pid] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}
        for _ in range(5):
            negamax.next_move('black', board)

        print()
        print(pid, 'depth = 3')
        print(' min :', Measure.elp_time[pid]['min'], '(s)')
        print(' max :', Measure.elp_time[pid]['max'], '(s)')
        print(' ave :', Measure.elp_time[pid]['ave'], '(s)')

    def test_negamax_timer_timeout(self):
        board = BitBoard()
        board.put_disc('black', 3, 2)
        negamax = NegaMax(depth=10, evaluator=coord.Evaluator_TPOW())
        pid = negamax.__class__.__name__ + str(os.getpid())
        Measure.elp_time[pid] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}

        negamax.next_move('white', board)
        self.assertTrue(Timer.timeout_flag[pid])
        self.assertLessEqual(Measure.elp_time[pid]['max'], CPU_TIME * 1.1)
