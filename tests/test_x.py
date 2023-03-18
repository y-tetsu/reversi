"""Tests of x.py
"""

import unittest

from reversi.board import AbstractBoard, BoardSizeError, Board, BitBoard, PyBitBoard
from reversi.color import C as c
from reversi.disc import D as d
from reversi.move import Move
from reversi.x import X
from reversi.game import Game
from reversi.player import Player
from reversi.strategies import Random
from reversi.simulator import Simulator
from reversi.display import NoneDisplay


class TestX(unittest.TestCase):
    def test_board_hole(self):
        for key in X.keys():
            hole = X[key][0]
            ini_black = X[key][1]
            ini_white = X[key][2]
            aryboard = Board(hole=hole, ini_black=ini_black, ini_white=ini_white)
            pybitboard = PyBitBoard(hole=hole, ini_black=ini_black, ini_white=ini_white)
            bitboard = BitBoard(hole=hole, ini_black=ini_black, ini_white=ini_white)
            self.assertEqual(str(aryboard), str(pybitboard))
            self.assertEqual(str(aryboard), str(bitboard))
            print(bitboard)

        aryboard = Board(4)
        bitboard = BitBoard(4)
        pybitboard = PyBitBoard(4)
        self.assertEqual(str(aryboard), str(pybitboard))
        self.assertEqual(str(aryboard), str(bitboard))
        print(aryboard)

    def test_board_ini_green(self):
        hole      = 0x0F0F0F0F
        ini_black = 0x00FF00FF
        ini_white = 0x0000FFFF
        aryboard = Board(hole=hole, ini_black=ini_black, ini_white=ini_white)
        pybitboard = PyBitBoard(hole=hole, ini_black=ini_black, ini_white=ini_white)
        bitboard = BitBoard(hole=hole, ini_black=ini_black, ini_white=ini_white)
        self.assertEqual(str(aryboard), str(pybitboard))
        self.assertEqual(str(aryboard), str(bitboard))

    def test_board_ini(self):
        for board in [Board(), PyBitBoard(), BitBoard()]:
            self.assertEqual(board._ini_black, 0x0000000810000000)
            self.assertEqual(board._ini_white, 0x0000001008000000)
            self.assertEqual(board._black_score, 2)
            self.assertEqual(board._white_score, 2)

    def test_board_remain(self):
        name = 'x'
        ini_black = X[name][1]
        ini_white = X[name][2]
        board = Board(ini_black=ini_black, ini_white=ini_white, hole=X[name][0])
        print(board)
        self.assertEqual(board.get_remain(), 36)

        name = 'Torus'
        ini_black = X[name][1]
        ini_white = X[name][2]
        board = Board(ini_black=ini_black, ini_white=ini_white, hole=X[name][0])
        print(board)
        self.assertEqual(board.get_remain(), 44)

    def test_move(self):
        name = 'X'  # * Can not change *
        patterns = [
            (c.black, ['d3', 'e6']),
            (c.white, ['c3', 'e3']),
            (c.black, ['e6']),
            (c.white, ['e3', 'd6', 'f6']),
            (c.black, ['b2', 'c2']),
            (c.white, ['d6']),
        ]

        # (1)配列ボード
        board = Board(hole=X[name][0])
        for color, expected in patterns:
            moves = [str(Move(*m)) for m in board.get_legal_moves(color)]
            self.assertEqual(moves, expected)
            board.put_disc(color, *Move(moves[0]))

        # (2)ビットボード(Python版:低速)
        # ---
        import os
        import importlib
        import reversi
        os.environ['FORCE_BITBOARDMETHODS_IMPORT_ERROR'] = 'RAISE'
        importlib.reload(reversi.BitBoardMethods)
        # ---

        board = PyBitBoard(hole=X[name][0])
        for color, expected in patterns:
            moves = [str(Move(*m)) for m in board.get_legal_moves(color)]
            self.assertEqual(moves, expected)
            board.put_disc(color, *Move(moves[0]))

        # ---
        del os.environ['FORCE_BITBOARDMETHODS_IMPORT_ERROR']
        importlib.reload(reversi.BitBoardMethods)
        # ---

        # (3)ビットボード(Python版:高速)
        board = PyBitBoard(hole=X[name][0])
        for color, expected in patterns:
            moves = [str(Move(*m)) for m in board.get_legal_moves(color)]
            self.assertEqual(moves, expected)
            board.put_disc(color, *Move(moves[0]))

        # (4)ビットボード(Cython版)
        board = BitBoard(hole=X[name][0])
        for color, expected in patterns:
            moves = [str(Move(*m)) for m in board.get_legal_moves(color)]
            self.assertEqual(moves, expected)
            board.put_disc(color, *Move(moves[0]))

    def test_game(self):
        name = 'T'
        hole = X[name][0]
        ini_black = X[name][1]
        ini_white = X[name][2]
        #board = Board(hole=hole, ini_black=ini_black, ini_white=ini_white)
        #board = PyBitBoard(hole=hole, ini_black=ini_black, ini_white=ini_white)
        board = BitBoard(hole=hole, ini_black=ini_black, ini_white=ini_white)
        black = Player('black', 'Black', Random())
        white = Player('white', 'White', Random())
        game = Game(black, white, board=board, display=TestDisplay())
        game.play()
        print(game.result.black_num, " - ", game.result.white_num)

    def test_simulation(self):
        name = 'Torus'
        low_speed = False

        # ---
        if low_speed:
            import os
            import importlib
            import reversi
            os.environ['FORCE_BITBOARDMETHODS_IMPORT_ERROR'] = 'RAISE'
            importlib.reload(reversi.BitBoardMethods)
        # ---

        players_info = {'Black': Random(), 'White': Random()}
        simulator = Simulator(
                        players_info,
                        board_type='bitboard',
                        first='black',
                        board_hole=X[name][0],
                        ini_black=X[name][1],
                        ini_white=X[name][2],
                        random_opening=0,
                        swap=False,
                        matches=10,
                        perfect_check=True,
                    )
        simulator.start()
        print(simulator)

        # ---
        if low_speed:
            del os.environ['FORCE_BITBOARDMETHODS_IMPORT_ERROR']
            importlib.reload(reversi.BitBoardMethods)
        # ---



class TestDisplay:
    def progress(self, board, black_player, white_player):
        print('\n' + str(board))

    def turn(self, player, legal_moves):
        print(player, [str(Move(*move)) for move in legal_moves])

    def move(self, player, legal_moves):
        print(str(Move(*player.move)))

    def foul(self, player):
        print('*** foul ***', player)

    def win(self, player):
        print('--- win ---', player)

    def draw(self):
        print('draw')
