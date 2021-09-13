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
        print('(150000)', Measure.count[pid])

    def test_endgame_remain_12(self):
        # Windows10 Celeron 1.6GHz 4.00GB
        board = BitBoard()
        endgame = _EndGame(depth=12)
        key = endgame.__class__.__name__ + str(os.getpid())
        Measure.elp_time[key] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}
        color = 'black'
        board._black_bitboard = 0xF07DBF650158381C
        board._white_bitboard = 0x2009A7EA6C4E0
        board.update_score()
        self.assertEqual(endgame.next_move(color, board), (7, 0))
        print()
        print(key, 'remain = 12')
        print(' min :', Measure.elp_time[key]['min'], '(s)')
        print(' max :', Measure.elp_time[key]['max'], '(s)')
        print(' ave :', Measure.elp_time[key]['ave'], '(s)')
        print('(342795 / 0.38s)', Measure.count[key])

    #def test_endgame_remain_14(self):
    #    board = BitBoard()
    #    endgame = _EndGame(depth=14)
    #    key = endgame.__class__.__name__ + str(os.getpid())
    #    Measure.elp_time[key] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}
    #    color = 'black'
    #    board._black_bitboard = 0xE07DBF650158381C
    #    board._white_bitboard = 0x0009A7EA6C4E0
    #    board.update_score()
    #    self.assertEqual(endgame.next_move(color, board), (7, 5))
    #    print()
    #    print(key, 'remain = 14')
    #    print(' min :', Measure.elp_time[key]['min'], '(s)')
    #    print(' max :', Measure.elp_time[key]['max'], '(s)')
    #    print(' ave :', Measure.elp_time[key]['ave'], '(s)')
    #    print('(3360357 / 3.47s)', Measure.count[key])

    #def test_endgame_remain_16(self):
    #    board = BitBoard()
    #    endgame = _EndGame(depth=16)
    #    key = endgame.__class__.__name__ + str(os.getpid())
    #    Measure.elp_time[key] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}
    #    color = 'black'
    #    board._black_bitboard = 0xC07DBF650158381C
    #    board._white_bitboard = 0x0009A7CA6C4E0
    #    board.update_score()
    #    self.assertEqual(endgame.next_move(color, board), (6, 6))
    #    print()
    #    print(key, 'remain = 16')
    #    print(' min :', Measure.elp_time[key]['min'], '(s)')
    #    print(' max :', Measure.elp_time[key]['max'], '(s)')
    #    print(' ave :', Measure.elp_time[key]['ave'], '(s)')
    #    print('(42957816 / 49.44s)', Measure.count[key])

    def test_endgame_force_import_error(self):
        import os
        import importlib
        import reversi

        # -------------------------------
        # switch environ and reload module
        os.environ['FORCE_ENDGAMEMETHODS_IMPORT_ERROR'] = 'RAISE'
        importlib.reload(reversi.strategies.EndGameMethods)
        self.assertTrue(reversi.strategies.EndGameMethods.ENDGAME_SIZE8_64BIT_ERROR)
        # -------------------------------

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

        # -------------------------------
        # recover environment and reload module
        del os.environ['FORCE_ENDGAMEMETHODS_IMPORT_ERROR']
        importlib.reload(reversi.strategies.EndGameMethods)
        self.assertFalse(reversi.strategies.EndGameMethods.ENDGAME_SIZE8_64BIT_ERROR)
        # -------------------------------
