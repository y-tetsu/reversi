"""Tests of endgame.py
"""

import unittest
import os
import time

from reversi.board import BitBoard
from reversi.strategies.common import Timer, Measure, CPU_TIME
from reversi.strategies import _EndGame_, _EndGame, EndGame_, EndGame, _AlphaBeta_, _AlphaBeta, AlphaBeta_, AlphaBeta
import reversi.strategies.coordinator as coord


class TestEndGame(unittest.TestCase):
    """endgame
    """
    def test_endgame_init(self):
        alphabeta_n = [_AlphaBeta_, _AlphaBeta, AlphaBeta_, AlphaBeta]
        timer = [False, False, True, True]
        measure = [False, True, False, True]
        for index, instance in enumerate([_EndGame_, _EndGame, EndGame_, EndGame]):
            endgame = instance()
            self.assertEqual(endgame._MIN, -10000000)
            self.assertEqual(endgame._MAX, 10000000)
            self.assertTrue(isinstance(endgame.evaluator, coord.Evaluator_N_Fast))
            self.assertEqual(endgame.depth, 10)
            self.assertTrue(isinstance(endgame.alphabeta_n, alphabeta_n[index]))
            self.assertEqual(endgame.timer, timer[index])
            self.assertEqual(endgame.measure, measure[index])
        depth = 12
        for index, instance in enumerate([_EndGame_, _EndGame, EndGame_, EndGame]):
            endgame = instance(depth)
            self.assertEqual(endgame._MIN, -10000000)
            self.assertEqual(endgame._MAX, 10000000)
            self.assertTrue(isinstance(endgame.evaluator, coord.Evaluator_N_Fast))
            self.assertEqual(endgame.depth, depth)
            self.assertTrue(isinstance(endgame.alphabeta_n, alphabeta_n[index]))
            self.assertEqual(endgame.timer, timer[index])
            self.assertEqual(endgame.measure, measure[index])

    def test_endgame_next_move(self):
        for instance in [_EndGame_, _EndGame, EndGame_, EndGame]:
            board = BitBoard()
            endgame = instance(depth=6)

            board.put_disc('black', 3, 2)
            self.assertEqual(endgame.next_move('white', board), (2, 2))

            board.put_disc('white', 2, 4)
            board.put_disc('black', 5, 5)
            board.put_disc('white', 4, 2)
            board.put_disc('black', 5, 2)
            board.put_disc('white', 5, 4)
            self.assertEqual(endgame.next_move('black', board), (1, 5))

    def test_endgame_timer_timeout(self):
        board = BitBoard()
        board.put_disc('black', 3, 2)
        endgame = EndGame(depth=20)
        pid = endgame.__class__.__name__ + str(os.getpid())
        Measure.elp_time[pid] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}
        Measure.count[pid] = 0
        endgame.next_move('white', board)
        self.assertTrue(Timer.timeout_flag[pid])
        self.assertLessEqual(Measure.elp_time[pid]['max'], CPU_TIME * 1.1)
        print('(180000)', Measure.count[pid])

    #def test_alphabeta_force_import_error(self):
    #    import os
    #    import importlib
    #    import reversi

    #    # -------------------------------
    #    # switch environ and reload module
    #    os.environ['FORCE_ALPHABETAMETHODS_IMPORT_ERROR'] = 'RAISE'
    #    importlib.reload(reversi.strategies.AlphaBetaMethods)
    #    self.assertTrue(reversi.strategies.AlphaBetaMethods.SLOW_MODE)
    #    self.assertTrue(reversi.strategies.AlphaBetaMethods.ALPHABETA_SIZE8_64BIT_ERROR)
    #    # -------------------------------

    #    # measure
    #    pid = 'ALPHABETA_IMPORT_ERROR_MEASURE'
    #    for _ in range(3):
    #        reversi.strategies.AlphaBetaMethods.GetScore.measure(pid)
    #    self.assertEqual(Measure.count[pid], 3)

    #    # timer
    #    pid = 'ALPHABETA_IMPORT_ERROR_TIMER'
    #    Timer.deadline[pid] = 0
    #    Timer.timeout_value[pid] = 100
    #    self.assertIsNone(reversi.strategies.AlphaBetaMethods.GetScore.timer(None))
    #    self.assertEqual(reversi.strategies.AlphaBetaMethods.GetScore.timer(pid), 100)
    #    self.assertTrue(Timer.timeout_flag[pid])

    #    # get_score
    #    alphabeta = AlphaBeta(depth=2, evaluator=coord.Evaluator_N())
    #    color = 'black'
    #    board = BitBoard(4)
    #    alpha = 1
    #    beta = 1
    #    depth = 0
    #    pid = 'ALPHABETA_IMPORT_ERROR_GET_SCORE'

    #    # - depth == 0
    #    score = reversi.strategies.AlphaBetaMethods.GetScore.get_score(alphabeta, color, board, alpha, beta, depth, pid)
    #    self.assertEqual(score, 0)

    #    # - pass and score
    #    depth = 1
    #    board._black_bitboard = 0x4000
    #    board._white_bitboard = 0x8000
    #    score = reversi.strategies.AlphaBetaMethods.GetScore.get_score(alphabeta, color, board, alpha, beta, depth, pid)
    #    self.assertEqual(score, -3)

    #    # get_score_measure
    #    score = reversi.strategies.AlphaBetaMethods.GetScore.get_score_measure(alphabeta, color, board, alpha, beta, depth, pid)
    #    self.assertEqual(score, -3)
    #    self.assertEqual(Measure.count[pid], 3)

    #    # get_score_timer
    #    Timer.deadline[pid] = 0
    #    Timer.timeout_value[pid] = 100
    #    score = reversi.strategies.AlphaBetaMethods.GetScore.get_score_timer(alphabeta, color, board, alpha, beta, depth, pid)
    #    self.assertEqual(score, 100)
    #    self.assertTrue(Timer.timeout_flag[pid])

    #    Timer.deadline[pid] = time.time() + 1
    #    score = reversi.strategies.AlphaBetaMethods.GetScore.get_score_timer(alphabeta, color, board, alpha, beta, depth, pid)
    #    self.assertEqual(score, 1)

    #    # get_score_measure_timer
    #    Measure.count[pid] = 0
    #    Timer.deadline[pid] = time.time() + 1
    #    score = reversi.strategies.AlphaBetaMethods.GetScore.get_score_measure_timer(alphabeta, color, board, alpha, beta, depth, pid)
    #    self.assertEqual(score, 1)
    #    self.assertEqual(Measure.count[pid], 3)

    #    # -------------------------------
    #    # recover environment and reload module
    #    del os.environ['FORCE_ALPHABETAMETHODS_IMPORT_ERROR']
    #    importlib.reload(reversi.strategies.AlphaBetaMethods)
    #    self.assertFalse(reversi.strategies.AlphaBetaMethods.SLOW_MODE)
    #    self.assertFalse(reversi.strategies.AlphaBetaMethods.ALPHABETA_SIZE8_64BIT_ERROR)
    #    # -------------------------------
