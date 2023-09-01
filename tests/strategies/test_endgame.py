"""Tests of endgame.py
"""

import unittest
import os

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
            self.assertEqual(endgame.depth, 60)
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

    def test_endgame_get_best_move(self):
        endgame = _EndGame_()

        # O--OOOOX
        # -OOOOOOX
        # OOXXOOOX
        # OOXOOOXX
        # OOOOOOXX
        # ---OOOOX
        # ----O--X
        # --------
        # X
        board = BitBoard()
        board._black_bitboard = 0x0101312303010100
        board._white_bitboard = 0x9E7ECEDCFC1E0800
        board.update_score()

        # depth=20 : black : a2
        board.put_disc('black', 0, 1)

        # depth=19 : white : b1
        board.put_disc('white', 1, 0)

        # depth=18 : black : c1
        board.put_disc('black', 2, 0)

        # depth=17 : white : --
        # depth=17 : black : b6
        board.put_disc('black', 1, 5)
        # print(board)
        # print(board._black_score, board._white_score)

        # depth=16 : white : c7
        self.assertEqual(endgame.get_best_move('white', board, board.get_legal_moves('white')), ((1, 6), {(1, 6): -38.0, (2, 6): -38.0}))
        board.put_disc('white', 2, 6)

        # depth=15 : black : a7
        self.assertEqual(endgame.get_best_move('black', board, board.get_legal_moves('black')), ((0, 6), {(0, 5): 16.0, (0, 6): 38.0, (1, 7): 38.0, (2, 5): 30.0, (3, 6): 38.0, (3, 7): 38.0, (4, 7): 38.0, (5, 6): 38.0, (5, 7): 38.0, (6, 6): 38.0}))  # noqa: E501
        board.put_disc('black', 0, 6)

        # depth=14 : white : b7
        self.assertEqual(endgame.get_best_move('white', board, board.get_legal_moves('white')), ((1, 6), {(1, 6): -38.0}))
        board.put_disc('white', 1, 6)

        # depth=13 : black : b8
        self.assertEqual(endgame.get_best_move('black', board, board.get_legal_moves('black')), ((1, 7), {(0, 5): 8.0, (1, 7): 38.0, (2, 5): 36.0, (3, 6): 36.0, (3, 7): 38.0, (4, 7): 38.0, (5, 6): 36.0, (5, 7): 38.0, (6, 6): 36.0}))  # noqa: E501
        board.put_disc('black', 1, 7)

        # depth=12 : white : d7
        self.assertEqual(endgame.get_best_move('white', board, board.get_legal_moves('white')), ((3, 6), {(2, 5): -42.0, (3, 6): -38.0, (3, 7): -38.0}))
        board.put_disc('white', 3, 6)

        # depth=11 : black : f8
        self.assertEqual(endgame.get_best_move('black', board, board.get_legal_moves('black')), ((5, 7), {(0, 5): 2.0, (2, 5): 36.0, (2, 7): 36.0, (3, 7): 36.0, (4, 7): 36.0, (5, 6): 36.0, (5, 7): 38.0, (6, 6): 36.0}))  # noqa: E501
        board.put_disc('black', 5, 7)

        # depth=10 : white : c6
        self.assertEqual(endgame.get_best_move('white', board, board.get_legal_moves('white')), ((2, 5), {(2, 5): -38.0, (3, 7): -38.0, (4, 7): -38.0, (5, 6): -38.0}))  # noqa: E501
        board.put_disc('white', 2, 5)

        # depth=9 : black : f7
        self.assertEqual(endgame.get_best_move('black', board, board.get_legal_moves('black')), ((5, 6), {(0, 5): -8.0, (0, 7): 38.0, (2, 7): 38.0, (3, 7): 38.0, (5, 6): 38.0, (6, 6): 38.0}))  # noqa: E501
        board.put_disc('black', 5, 6)

        # depth=8 : white : g7
        self.assertEqual(endgame.get_best_move('white', board, board.get_legal_moves('white')), ((6, 6), {(4, 7): -38.0, (6, 6): -38.0, (6, 7): -38.0}))
        board.put_disc('white', 6, 6)

        # depth=7 : black : a8
        self.assertEqual(endgame.get_best_move('black', board, board.get_legal_moves('black')), ((0, 7), {(0, 5): 6.0, (0, 7): 38.0, (2, 7): 38.0, (3, 7): 38.0, (4, 7): 38.0, (6, 7): 38.0}))  # noqa: E501
        board.put_disc('black', 0, 7)

        # depth=6 : white : --
        # depth=6 : black : d8
        self.assertEqual(endgame.get_best_move('black', board, board.get_legal_moves('black')), ((3, 7), {(0, 5): 34.0, (2, 7): 34.0, (3, 7): 38.0, (4, 7): 38.0, (6, 7): 38.0}))  # noqa: E501
        board.put_disc('black', 3, 7)

        # depth=5 : white : e8
        self.assertEqual(endgame.get_best_move('white', board, board.get_legal_moves('white')), ((4, 7), {(4, 7): -38.0}))
        board.put_disc('white', 4, 7)

        # depth=4 : balck : c8
        self.assertEqual(endgame.get_best_move('black', board, board.get_legal_moves('black')), ((2, 7), {(0, 5): 22.0, (2, 7): 38.0, (6, 7): 38.0, (7, 7): 38.0}))  # noqa: E501
        board.put_disc('black', 2, 7)

        # depth=3 : white ; g8
        self.assertEqual(endgame.get_best_move('white', board, board.get_legal_moves('white')), ((6, 7), {(6, 7): -38.0}))
        board.put_disc('white', 6, 7)

        # depth=2 : balck : a6
        self.assertEqual(endgame.get_best_move('black', board, board.get_legal_moves('black')), ((0, 5), {(0, 5): 38.0, (7, 7): 38.0}))
        board.put_disc('black', 0, 5)

        # depth=1 : white : --
        # depth=1 : black : h8
        self.assertEqual(endgame.get_best_move('black', board, board.get_legal_moves('black')), ((7, 7), {(7, 7): 38.0}))

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
        print('(1300000)', Measure.count[pid])

    def test_endgame_remain_12(self):
        # Windows10 Celeron 1.6GHz 4.00GB
        board = BitBoard()
        endgame = _EndGame(depth=12)
        key = endgame.__class__.__name__ + str(os.getpid())
        Measure.elp_time[key] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}
        Measure.count[key] = 0
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
        print('(101890 / 0.02s)', Measure.count[key])

    def test_endgame_remain_14(self):
        board = BitBoard()
        endgame = _EndGame(depth=14)
        key = endgame.__class__.__name__ + str(os.getpid())
        Measure.elp_time[key] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}
        Measure.count[key] = 0
        color = 'black'
        board._black_bitboard = 0xE07DBF650158381C
        board._white_bitboard = 0x0009A7EA6C4E0
        board.update_score()
        self.assertEqual(endgame.next_move(color, board), (7, 5))
        print()
        print(key, 'remain = 14')
        print(' min :', Measure.elp_time[key]['min'], '(s)')
        print(' max :', Measure.elp_time[key]['max'], '(s)')
        print(' ave :', Measure.elp_time[key]['ave'], '(s)')
        print('(562957 / 0.08s)', Measure.count[key])

    def test_endgame_remain_16(self):
        board = BitBoard()
        endgame = _EndGame(depth=16)
        key = endgame.__class__.__name__ + str(os.getpid())
        Measure.elp_time[key] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}
        Measure.count[key] = 0
        color = 'black'
        board._black_bitboard = 0xC07DBF650158381C
        board._white_bitboard = 0x0009A7CA6C4E0
        board.update_score()
        self.assertEqual(endgame.next_move(color, board), (6, 6))
        print()
        print(key, 'remain = 16')
        print(' min :', Measure.elp_time[key]['min'], '(s)')
        print(' max :', Measure.elp_time[key]['max'], '(s)')
        print(' ave :', Measure.elp_time[key]['ave'], '(s)')
        print('(5417116 / 0.68s)', Measure.count[key])

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
