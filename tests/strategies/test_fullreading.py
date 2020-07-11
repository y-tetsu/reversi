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

    def test_fullreading_remain_10(self):
        class Test:
            pass

        board = BitBoard()
        fullreading = _FullReading(remain=10, base=Test())
        key = fullreading.__class__.__name__ + str(os.getpid())
        Measure.elp_time[key] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}
        color = 'black'

        board._black_bitboard = 0xF07DBF650158381E
        board._white_bitboard = 0x2009AFEA6C4E0
        board.update_score()
        self.assertEqual(fullreading.next_move(color, board), (7, 0))
        board._legal_moves_cache.clear()

        print()
        print(key, 'remain = 10')
        print(' min :', Measure.elp_time[key]['min'], '(s)')
        print(' max :', Measure.elp_time[key]['max'], '(s)')
        print(' ave :', Measure.elp_time[key]['ave'], '(s)')
