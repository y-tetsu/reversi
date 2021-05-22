"""Tests of negascout.py
"""

import unittest
import os
import time

from reversi.board import BitBoard
from reversi.strategies.common import Timer, Measure, CPU_TIME
from reversi.strategies import _NegaScout_, _NegaScout, NegaScout_, NegaScout
import reversi.strategies.coordinator as coord


NEGASCOUT_CLASSES = [_NegaScout_, _NegaScout, NegaScout_, NegaScout]


class TestNegaScout(unittest.TestCase):
    """negascout
    """
    def test_negascout_init(self):
        for class_name in NEGASCOUT_CLASSES:
            negascout = class_name()
            self.assertEqual(negascout._MIN, -10000000)
            self.assertEqual(negascout._MAX, 10000000)
            self.assertEqual(negascout.depth, 3)
            self.assertEqual(negascout.evaluator, None)

            negascout = class_name(depth=4, evaluator=coord.Evaluator_T())
            self.assertEqual(negascout._MIN, -10000000)
            self.assertEqual(negascout._MAX, 10000000)
            self.assertEqual(negascout.depth, 4)
            self.assertTrue(isinstance(negascout.evaluator, coord.Evaluator_T))

    def test_negascout_get_score(self):
        for class_name in NEGASCOUT_CLASSES:
            board = BitBoard()
            negascout = class_name(evaluator=coord.Evaluator_T())
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
        for class_name in NEGASCOUT_CLASSES:
            board = BitBoard()
            negascout = class_name(evaluator=coord.Evaluator_TPOW())

            board.put_disc('black', 3, 2)
            self.assertEqual(negascout.next_move('white', board), (2, 4))

            board.put_disc('white', 2, 4)
            board.put_disc('black', 5, 5)
            board.put_disc('white', 4, 2)
            board.put_disc('black', 5, 2)
            board.put_disc('white', 5, 4)
            self.assertEqual(negascout.next_move('black', board), (2, 2))

    def test_negascout_get_best_move(self):
        for class_name in NEGASCOUT_CLASSES:
            board = BitBoard()
            negascout = class_name(evaluator=coord.Evaluator_TPW())

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
        pid = negascout.__class__.__name__ + str(os.getpid())

        Measure.count[pid] = 0
        Timer.timeout_flag[pid] = False
        Timer.timeout_value[pid] = 0
        Timer.deadline[pid] = time.time() + CPU_TIME
        score = negascout._get_score('white', board, negascout._MIN, negascout._MAX, 5, pid=pid)  # depth 5
        self.assertEqual(score, 4)
        self.assertEqual(Measure.count[pid], 293)

        # _NegaScout
        negascout = _NegaScout(evaluator=coord.Evaluator_TPOW())
        pid = negascout.__class__.__name__ + str(os.getpid())

        Measure.count[pid] = 0
        score = negascout._get_score('white', board, negascout._MIN, negascout._MAX, 2, pid=pid)  # depth 2
        self.assertEqual(score, -10.75)
        self.assertEqual(Measure.count[pid], 20)

        Measure.count[pid] = 0
        score = negascout._get_score('white', board, negascout._MIN, negascout._MAX, 3, pid=pid)  # depth 3
        self.assertEqual(score, 6.25)
        self.assertEqual(Measure.count[pid], 76)

        Measure.count[pid] = 0
        score = negascout._get_score('white', board, negascout._MIN, negascout._MAX, 4, pid=pid)  # depth 4
        self.assertEqual(score, -8.25)
        self.assertEqual(Measure.count[pid], 295)

        Measure.count[pid] = 0
        score = negascout._get_score('white', board, negascout._MIN, negascout._MAX, 5, pid=pid)  # depth 5
        self.assertEqual(score, 4)
        self.assertEqual(Measure.count[pid], 293)

        Measure.count[pid] = 0
        score = negascout._get_score('white', board, negascout._MIN, negascout._MAX, 6, pid=pid)  # depth 6
        self.assertEqual(score, -3.5)
        self.assertEqual(Measure.count[pid], 1275)

        Measure.count[pid] = 0
        score = negascout._get_score('white', board, negascout._MIN, negascout._MAX, 7, pid=pid)  # depth 7
        self.assertEqual(score, 1.0)
        self.assertEqual(Measure.count[pid], 1596)

        board.put_disc('white', 2, 4)
        board.put_disc('black', 5, 5)
        board.put_disc('white', 4, 2)
        board.put_disc('black', 5, 2)
        board.put_disc('white', 5, 4)
        Measure.elp_time[pid] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}
        for _ in range(5):
            negascout.next_move('black', board)

        print()
        print(pid, 'depth = 3')
        print(' min :', Measure.elp_time[pid]['min'], '(s)')
        print(' max :', Measure.elp_time[pid]['max'], '(s)')
        print(' ave :', Measure.elp_time[pid]['ave'], '(s)')

        # best move
        class _NegaScoutTest(_NegaScout):
            @Measure.time
            def get_best_move(self, color, board, moves, depth):
                return super().get_best_move(color, board, moves, depth)

        negascout = _NegaScoutTest(evaluator=coord.Evaluator_TPOW())
        pid = negascout.__class__.__name__ + str(os.getpid())

        moves = board.get_legal_moves('black')
        Measure.elp_time[pid] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}
        for _ in range(3):
            negascout.get_best_move('black', board, moves, 4)

        print()
        print(pid, 'depth = 4')
        print(' min :', Measure.elp_time[pid]['min'], '(s)')
        print(' max :', Measure.elp_time[pid]['max'], '(s)')
        print(' ave :', Measure.elp_time[pid]['ave'], '(s)')
        self.assertEqual(negascout.get_best_move('black', board, moves, 4), ((5, 3), {(2, 2): -4.25, (2, 3): -3.75, (5, 3): -1.75, (1, 5): -1.75, (2, 5): -1.75, (3, 5): -1.75, (4, 5): -1.75, (6, 5): -1.75}))  # noqa: E501

        moves = coord.Orderer_B().move_ordering(color='black', board=board, moves=moves, best_move=(5, 3))
        Measure.elp_time[pid] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}
        for _ in range(3):
            negascout.get_best_move('black', board, moves, 4)

        print()
        print(pid, 'depth = 4 Orderer_B')
        print(' min :', Measure.elp_time[pid]['min'], '(s)')
        print(' max :', Measure.elp_time[pid]['max'], '(s)')
        print(' ave :', Measure.elp_time[pid]['ave'], '(s)')

    def test_negascout_timer_timeout(self):
        board = BitBoard()
        board.put_disc('black', 3, 2)
        negascout = NegaScout(depth=10, evaluator=coord.Evaluator_TPOW())
        pid = negascout.__class__.__name__ + str(os.getpid())
        Measure.elp_time[pid] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}
        Measure.count[pid] = 0

        negascout.next_move('white', board)
        self.assertTrue(Timer.timeout_flag[pid])
        self.assertLessEqual(Measure.elp_time[pid]['max'], CPU_TIME * 1.1)
        print('(7000)', Measure.count[pid])

    def test_negascout_force_import_error(self):
        import os
        import importlib
        import reversi

        # -------------------------------
        # switch environ and reload module
        os.environ['FORCE_NEGASCOUTMETHODS_IMPORT_ERROR'] = 'RAISE'
        importlib.reload(reversi.strategies.NegaScoutMethods)
        self.assertTrue(reversi.strategies.NegaScoutMethods.SLOW_MODE)
        # -------------------------------

        # measure
        pid = 'NEGASCOUT_IMPORT_ERROR_MEASURE'
        for _ in range(3):
            reversi.strategies.NegaScoutMethods.GetScore.measure(pid)
        self.assertEqual(Measure.count[pid], 3)

        # timer
        pid = 'NEGASCOUT_IMPORT_ERROR_TIMER'
        Timer.deadline[pid] = 0
        Timer.timeout_value[pid] = 100
        self.assertIsNone(reversi.strategies.NegaScoutMethods.GetScore.timer(None))
        self.assertEqual(reversi.strategies.NegaScoutMethods.GetScore.timer(pid), 100)
        self.assertTrue(Timer.timeout_flag[pid])

        # get_score
        negascout = NegaScout(depth=2, evaluator=coord.Evaluator_N())
        color = 'black'
        board = BitBoard(4)
        alpha = -10
        beta = 1
        depth = 0
        pid = 'NEGASCOUT_IMPORT_ERROR_GET_SCORE'

        # - depth == 0
        score = reversi.strategies.NegaScoutMethods.GetScore.get_score(negascout, color, board, alpha, beta, depth, pid)
        self.assertEqual(score, 0)

        # - pass and score
        depth = 1
        board._black_bitboard = 0x4000
        board._white_bitboard = 0x8000
        score = reversi.strategies.NegaScoutMethods.GetScore.get_score(negascout, color, board, alpha, beta, depth, pid)
        self.assertEqual(score, -3)

        # - alpha >= beta
        beta = -10
        score = reversi.strategies.NegaScoutMethods.GetScore.get_score(negascout, color, board, alpha, beta, depth, pid)
        self.assertEqual(score, -10)

        # - tmp <= null_wndow
        board = BitBoard(8)
        board.put_disc('black', 5, 4)
        board.put_disc('white', 3, 5)
        board.put_disc('black', 2, 5)
        depth = 3
        alpha = -100
        beta = 100
        Timer.timeout_flag[pid] = True
        score = reversi.strategies.NegaScoutMethods.GetScore.get_score(negascout, color, board, alpha, beta, depth, pid)
        self.assertEqual(score, 6)

        # get_score_measure
        board = BitBoard(4)
        board._black_bitboard = 0x4000
        board._white_bitboard = 0x8000
        beta = 1
        Measure.count[pid] = 0
        score = reversi.strategies.NegaScoutMethods.GetScore.get_score_measure(negascout, color, board, alpha, beta, depth, pid)
        self.assertEqual(score, -3)
        self.assertEqual(Measure.count[pid], 3)

        # get_score_timer
        Timer.deadline[pid] = 0
        Timer.timeout_value[pid] = 100
        score = reversi.strategies.NegaScoutMethods.GetScore.get_score_timer(negascout, color, board, alpha, beta, depth, pid)
        self.assertEqual(score, 100)
        self.assertTrue(Timer.timeout_flag[pid])

        Timer.deadline[pid] = time.time() + 1
        score = reversi.strategies.NegaScoutMethods.GetScore.get_score_timer(negascout, color, board, alpha, beta, depth, pid)
        self.assertEqual(score, -3)

        # get_score_measure_timer
        Measure.count[pid] = 0
        Timer.deadline[pid] = time.time() + 1
        score = reversi.strategies.NegaScoutMethods.GetScore.get_score_measure_timer(negascout, color, board, alpha, beta, depth, pid)
        self.assertEqual(score, -3)
        self.assertEqual(Measure.count[pid], 3)

        # -------------------------------
        # recover environment and reload module
        del os.environ['FORCE_NEGASCOUTMETHODS_IMPORT_ERROR']
        importlib.reload(reversi.strategies.NegaScoutMethods)
        self.assertFalse(reversi.strategies.NegaScoutMethods.SLOW_MODE)
        # -------------------------------
