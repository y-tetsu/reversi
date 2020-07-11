"""Tests of fullreading.py
"""

import unittest
import os

from reversi.board import BitBoard
from reversi.strategies import _FullReading, FullReading
from reversi.strategies.alphabeta import _AlphaBeta_N, AlphaBeta_N
from reversi.strategies.common import Measure


class TestFullReading(unittest.TestCase):
    """fullreading
    """
    def test_fullreading_init(self):
        class Test:
            pass

        remain = 3
        fullreading = FullReading(remain=remain, base=Test())
        _fullreading = _FullReading(remain=remain, base=Test())

        self.assertEqual(fullreading.remain, remain)
        self.assertTrue(isinstance(fullreading.base, Test))
        self.assertTrue(isinstance(fullreading.fullreading, AlphaBeta_N))
        self.assertEqual(fullreading.fullreading.depth, remain)

        self.assertEqual(_fullreading.remain, remain)
        self.assertTrue(isinstance(_fullreading.base, Test))
        self.assertTrue(isinstance(_fullreading.fullreading, _AlphaBeta_N))
        self.assertEqual(_fullreading.fullreading.depth, remain)

    def test_fullreading_next_move(self):
        class Test:
            def next_move(self, color, board):
                return (3, 3)

        board = BitBoard()
        fullreading = _FullReading(remain=8, base=Test())

        color = 'white'
        board._black_bitboard = 0x3FFFEE3E192CC07E
        board._white_bitboard = 0x400011C0E4523900
        board.update_score()

        # remain = 9 : base
        self.assertEqual(fullreading.next_move(color, board), (3, 3))

        # remain = 8 : fullreading
        board.put_disc(color, 0, 0)
        color = 'black'
        self.assertEqual(fullreading.next_move(color, board), (7, 5))

    def test_fullreading_remain_9(self):
        class Test:
            pass

        board = BitBoard()
        fullreading = _FullReading(remain=9, base=Test())
        key = fullreading.__class__.__name__ + str(os.getpid())
        Measure.elp_time[key] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}
        color = 'white'

        # pattern 1
        board._black_bitboard = 0x3FFFEE3E192CC07E
        board._white_bitboard = 0x400011C0E4523900
        board.update_score()
        self.assertEqual(fullreading.next_move(color, board), (0, 0))
        board._legal_moves_cache.clear()

        # pattern 2
        board._black_bitboard = 0x81878F170B470000
        board._white_bitboard = 0x7C387068F4381F3F
        board.update_score()
        self.assertEqual(fullreading.next_move(color, board), (6, 0))
        board._legal_moves_cache.clear()

        # pattern 3
        board._black_bitboard = 0xF27FBF650158381E
        board._white_bitboard = 0x9AFEA6C4E0
        board.update_score()
        self.assertEqual(fullreading.next_move(color, board), (7, 7))
        board._legal_moves_cache.clear()

        # pattern 4
        board._black_bitboard = 0x5C2353046C3874BA
        board._white_bitboard = 0x80DCACFB93850B00
        board.update_score()
        self.assertEqual(fullreading.next_move(color, board), (7, 0))
        board._legal_moves_cache.clear()

        # pattern 5
        board._black_bitboard = 0x828522161C1C07FF
        board._white_bitboard = 0x4858DC69E3E3B800
        board.update_score()
        self.assertEqual(fullreading.next_move(color, board), (7, 2))
        board._legal_moves_cache.clear()

        print()
        print(key, 'remain = 9')
        print(' min :', Measure.elp_time[key]['min'], '(s)')
        print(' max :', Measure.elp_time[key]['max'], '(s)')
        print(' ave :', Measure.elp_time[key]['ave'], '(s)')

    def test_fullreading_generate_pattern(self):
        class Test:
            def next_move(self, color, board):
                return (0, 0)

        from reversi.strategies.easy import Random
        from reversi.game import Game
        from reversi.player import Player
        from reversi.display import NoneDisplay

        board = BitBoard()
        game = Game(board, Player('black', 'B', Random()), Player('white', 'W', Random()), NoneDisplay())
        game.play()

        #print(board)

        prev = None
        for _ in range(9):
            prev = board.undo()

        #print()
        #print(9)
        #print(board)
        #print("color = '{}'".format(prev['color']))
        #print('board._black_bitboard = 0x{:X}\nboard._white_bitboard = 0x{:X}'.format(*board.get_bitboard_info()))

        #color = white
        #board._black_bitboard = 0x3FFFEE3E192CC07E
        #board._white_bitboard = 0x400011C0E4523900
        #board._black_bitboard = 0x81878F170B470000
        #board._white_bitboard = 0x7C387068F4381F3F
        #board._black_bitboard = 0xF27FBF650158381E
        #board._white_bitboard = 0x9AFEA6C4E0
        #board._black_bitboard = 0x5C2353046C3874BA
        #board._white_bitboard = 0x80DCACFB93850B00
        #board._black_bitboard = 0x828522161C1C07FF
        #board._white_bitboard = 0x4858DC69E3E3B800

        #prev = board.undo()
        #print()
        #print(10)
        #print(board)
        #print("color = '{}'".format(prev['color']))
        #print('board._black_bitboard = 0x{:X}\nboard._white_bitboard = 0x{:X}'.format(*board.get_bitboard_info()))

        #color = black
        #board._black_bitboard = 0x3FFFEE3C182CC07E
        #board._white_bitboard = 0x400011C2E4523900

        #color = black
        #board._black_bitboard = 0x1078F170B470000
        #board._white_bitboard = 0x7CB87068F4381F3F

        #color = black
        #board._black_bitboard = 0xF07DBF650158381E
        #board._white_bitboard = 0x2009AFEA6C4E0

        #color = 'black'
        #board._black_bitboard = 0x5C225100642874BA
        #board._white_bitboard = 0x80DCAEFF9B950B00

        #color = 'black'
        #board._black_bitboard = 0x828522161C1C0707
        #board._white_bitboard = 0x4858DC69E3E3B878

        #prev = board.undo()
        #print()
        #print(11)
        #print(board)
        #print("color = '{}'".format(prev['color']))
        #print('board._black_bitboard = 0x{:X}\nboard._white_bitboard = 0x{:X}'.format(*board.get_bitboard_info()))

        #color = white
        #board._black_bitboard = 0x3FFFEE3C182EC07E
        #board._white_bitboard = 0x400011C2E4503800

        #color = white
        #board._black_bitboard = 0x1078F372B470000
        #board._white_bitboard = 0x7CB87048D4181F3F

        #color = white
        #board._black_bitboard = 0xF07DBF6579D8381E
        #board._white_bitboard = 0x2009A0626C4E0

        #color = 'white'
        #board._black_bitboard = 0x5C225102642874BA
        #board._white_bitboard = 0x80DCACFD9B950B00

        #color = 'white'
        #board._black_bitboard = 0x82852A161C1C0707
        #board._white_bitboard = 0x4850D469E3E3B878

        #prev = board.undo()
        #print()
        #print(12)
        #print(board)
        #print("color = '{}'".format(prev['color']))
        #print('board._black_bitboard = 0x{:X}\nboard._white_bitboard = 0x{:X}'.format(*board.get_bitboard_info()))

        #color = black
        #board._black_bitboard = 0x3F3FAE1C182EC07E
        #board._white_bitboard = 0x404051E2E4503800

        #color = black
        #board._black_bitboard = 0x1078F3729440000
        #board._white_bitboard = 0x7CB87048D61A1F3F

        #color = black
        #board._black_bitboard = 0xF07DBF6579D80802
        #board._white_bitboard = 0x2009A0626F4EC

        #color = 'black'
        #board._black_bitboard = 0x5C225102642870B8
        #board._white_bitboard = 0x80DCACFD9B950F00

        #color = 'black'
        #board._black_bitboard = 0x828428121C1C0707
        #board._white_bitboard = 0x4850D66DE3E3B878
