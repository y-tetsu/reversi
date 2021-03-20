"""Tests of joseki.py
"""

import unittest
import os

from reversi import C as c
from reversi.board import BitBoard
from reversi.strategies import AbstractStrategy, Random, _Joseki_, _Usagi_, Usagi, _Tora_, Tora, _Ushi_, Ushi, _Nezumi_, Nezumi, _Neko_, Neko
from reversi.strategies.common import Measure
from reversi.strategies.joseki import MOUSE, BULL, TIGER, SROSE, ROSEVILLE, FASTBOAT, CAT, RABBIT, SHEEP


# def rotate_180(bbits, wbits, move):  # 180°回転
#     bbits_tmp = [['0' for i in range(8)] for j in range(8)]
#     wbits_tmp = [['0' for i in range(8)] for j in range(8)]
#
#     check = 1 << 63
#     for y in range(8):
#         for x in range(8):
#             if bbits & check:
#                 bbits_tmp[y][x] = '1'
#             if wbits & check:
#                 wbits_tmp[y][x] = '1'
#             check >>= 1
#
#     import numpy as np
#
#     bbits_tmp = np.rot90(np.rot90(np.array(bbits_tmp)))
#     wbits_tmp = np.rot90(np.rot90(np.array(wbits_tmp)))
#     bbits = int(''.join(bbits_tmp.flatten()), 2)
#     wbits = int(''.join(wbits_tmp.flatten()), 2)
#     move = 7 - move[0], 7 - move[1]
#
#     return bbits, wbits, move
#
# def delta_swap(bits, mask, delta):
#     x = (bits ^ (bits >> delta)) & mask
#     return bits ^ x ^ (x << delta)
#
# def flip_diag(bbits, wbits, move):  # 対角線を軸に反転
#     bbits = delta_swap(bbits, 0x00000000F0F0F0F0, 28)
#     bbits = delta_swap(bbits, 0x0000CCCC0000CCCC, 14)
#     bbits = delta_swap(bbits, 0x00AA00AA00AA00AA,  7)
#     wbits = delta_swap(wbits, 0x00000000F0F0F0F0, 28)
#     wbits = delta_swap(wbits, 0x0000CCCC0000CCCC, 14)
#     wbits = delta_swap(wbits, 0x00AA00AA00AA00AA,  7)
#     move = move[1], move[0]
#     return bbits, wbits, move
#
# def rotate_flip(color, b, w, move):
#     print(f"    ('{color}', 0x{b:016X}, 0x{w:016X}): {move},")
#     b2, w2, move2 = rotate_180(b, w, move)
#     print(f"    ('{color}', 0x{b2:016X}, 0x{w2:016X}): {move2},")
#     b3, w3, move3 = flip_diag(b, w, move)
#     print(f"    ('{color}', 0x{b3:016X}, 0x{w3:016X}): {move3},")
#     b4, w4, move4 = flip_diag(b2, w2, move2)
#     print(f"    ('{color}', 0x{b4:016X}, 0x{w4:016X}): {move4},")


class TestJoseki(unittest.TestCase):
    """joseki
    """
    def test_joseki_init(self):
        joseki = _Joseki_(Random())

        self.assertEqual(joseki.joseki, {})
        self.assertIsInstance(joseki.base, Random)

    def test_joseki_next_move(self):
        class Origin(AbstractStrategy):
            def next_move(self, color, board):
                return (0, 0)

        joseki = _Joseki_(Origin())
        board = BitBoard(4)
        self.assertEqual(joseki.next_move(c.black, board), (0, 0))

        board = BitBoard(8)
        self.assertEqual(joseki.next_move(c.black, board), (0, 0))

        joseki.joseki = {
            (c.black, 0x0000000810000000, 0x0000001008000000): (5, 4),
        }
        self.assertEqual(joseki.next_move(c.black, board), (5, 4))

    def test_usagi_init(self):
        joseki = {}
        joseki.update(MOUSE)
        joseki.update(BULL)
        joseki.update(TIGER)
        joseki.update(SROSE)
        joseki.update(ROSEVILLE)
        joseki.update(FASTBOAT)
        joseki.update(CAT)
        joseki.update(RABBIT)

        # no Measure
        _usagi_ = _Usagi_(Random())
        key = _usagi_.__class__.__name__ + str(os.getpid())
        board = BitBoard()
        _usagi_.next_move(c.black, board)

        self.assertEqual(_usagi_.joseki, joseki)
        self.assertIsInstance(_usagi_.base, Random)
        self.assertFalse(key in Measure.elp_time)

        # with Measure
        usagi = Usagi(Random())
        key = usagi.__class__.__name__ + str(os.getpid())
        board = BitBoard()
        usagi.next_move(c.black, board)

        self.assertEqual(usagi.joseki, joseki)
        self.assertIsInstance(usagi.base, Random)
        self.assertTrue(key in Measure.elp_time)

    def test_usagi_next_move(self):
        board = BitBoard()
        usagi = Usagi(Random())
        patterns = [
            # turn,   move
            # --- 兎定石 ---
            (c.black, (5, 4)),
            (c.white, (3, 5)),
            (c.black, (2, 4)),
            (c.white, (5, 3)),
            (c.black, (4, 2)),
            # --- Sローズ基本形 ---
            (c.white, (2, 5)),
            (c.black, (3, 2)),
            (c.white, (5, 5)),
            (c.black, (4, 5)),
            (c.white, (3, 6)),
            (c.black, (6, 2)),
            (c.white, (2, 3)),
        ]
        for turn, expected in patterns:
            move = usagi.next_move(turn, board)
            board.put_disc(turn, *move)
            self.assertEqual(move, expected)

    def test_tora_init(self):
        joseki = {}
        joseki.update(MOUSE)
        joseki.update(BULL)
        joseki.update(RABBIT)
        joseki.update(SROSE)
        joseki.update(ROSEVILLE)
        joseki.update(FASTBOAT)
        joseki.update(CAT)
        joseki.update(TIGER)

        # no Measure
        _tora_ = _Tora_(Random())
        key = _tora_.__class__.__name__ + str(os.getpid())
        board = BitBoard()
        _tora_.next_move(c.black, board)

        self.assertEqual(_tora_.joseki, joseki)
        self.assertIsInstance(_tora_.base, Random)
        self.assertFalse(key in Measure.elp_time)

        # with Measure
        tora = Tora(Random())
        key = tora.__class__.__name__ + str(os.getpid())
        board = BitBoard()
        tora.next_move(c.black, board)

        self.assertEqual(tora.joseki, joseki)
        self.assertIsInstance(tora.base, Random)
        self.assertTrue(key in Measure.elp_time)

    def test_tora_next_move(self):
        board = BitBoard()
        tora = Tora(Random())
        patterns = [
            # turn,   move
            # --- 虎定石 ---
            (c.black, (5, 4)),
            (c.white, (3, 5)),
            (c.black, (2, 2)),
            # --- ローズビル基本形 ---
            (c.white, (3, 2)),
            (c.black, (2, 3)),
            (c.white, (5, 3)),
            (c.black, (2, 4)),
            (c.white, (1, 2)),
            (c.black, (2, 1)),
        ]
        for turn, expected in patterns:
            move = tora.next_move(turn, board)
            board.put_disc(turn, *move)
            self.assertEqual(move, expected)

    def test_ushi_init(self):
        joseki = {}
        joseki.update(RABBIT)
        joseki.update(CAT)
        joseki.update(TIGER)
        joseki.update(MOUSE)
        joseki.update(SROSE)
        joseki.update(ROSEVILLE)
        joseki.update(FASTBOAT)
        joseki.update(BULL)

        # no Measure
        _ushi_ = _Ushi_(Random())
        key = _ushi_.__class__.__name__ + str(os.getpid())
        board = BitBoard()
        _ushi_.next_move(c.black, board)

        self.assertEqual(_ushi_.joseki, joseki)
        self.assertIsInstance(_ushi_.base, Random)
        self.assertFalse(key in Measure.elp_time)

        # with Measure
        ushi = Ushi(Random())
        key = ushi.__class__.__name__ + str(os.getpid())
        board = BitBoard()
        ushi.next_move(c.black, board)

        self.assertEqual(ushi.joseki, joseki)
        self.assertIsInstance(ushi.base, Random)
        self.assertTrue(key in Measure.elp_time)

    def test_ushi_next_move(self):
        board = BitBoard()
        ushi = Ushi(Random())
        patterns = [
            # turn,   move
            # --- 牛定石 ---
            (c.black, (5, 4)),
            (c.white, (5, 5)),
            (c.black, (4, 5)),
            (c.white, (5, 3)),
            (c.black, (4, 2)),
            (c.white, (2, 4)),
            # --- 快速船基礎形 ---
            (c.black, (2, 3)),
            (c.white, (4, 6)),
            (c.black, (2, 5)),
            (c.white, (4, 1)),
            (c.black, (5, 2)),
            (c.white, (5, 1)),
        ]
        for turn, expected in patterns:
            move = ushi.next_move(turn, board)
            board.put_disc(turn, *move)
            self.assertEqual(move, expected)

    def test_nezumi_init(self):
        joseki = {}
        joseki.update(RABBIT)
        joseki.update(CAT)
        joseki.update(TIGER)
        joseki.update(BULL)
        joseki.update(SROSE)
        joseki.update(ROSEVILLE)
        joseki.update(FASTBOAT)
        joseki.update(MOUSE)

        # no Measure
        _nezumi_ = _Nezumi_(Random())
        key = _nezumi_.__class__.__name__ + str(os.getpid())
        board = BitBoard()
        _nezumi_.next_move(c.black, board)

        self.assertEqual(_nezumi_.joseki, joseki)
        self.assertIsInstance(_nezumi_.base, Random)
        self.assertFalse(key in Measure.elp_time)

        # with Measure
        nezumi = Nezumi(Random())
        key = nezumi.__class__.__name__ + str(os.getpid())
        board = BitBoard()
        nezumi.next_move(c.black, board)

        self.assertEqual(nezumi.joseki, joseki)
        self.assertIsInstance(nezumi.base, Random)
        self.assertTrue(key in Measure.elp_time)

    def test_nezumi_next_move(self):
        board = BitBoard()
        nezumi = Nezumi(Random())
        patterns = [
            # turn,   move
            # --- 鼠定石 ---
            (c.black, (5, 4)),
            (c.white, (5, 3)),
            (c.black, (4, 2)),
            (c.white, (5, 5)),
            (c.black, (3, 2)),
            (c.white, (2, 4)),
            (c.black, (3, 5)),
            (c.white, (2, 3)),
            (c.black, (4, 5)),
            (c.white, (2, 6)),
            (c.black, (3, 6)),
            (c.white, (2, 5)),
            (c.black, (6, 4)),
            (c.white, (6, 2)),
            (c.black, (5, 2)),
            (c.white, (3, 1)),
            (c.black, (2, 1)),
            (c.white, (4, 6)),
        ]
        for turn, expected in patterns:
            move = nezumi.next_move(turn, board)
            board.put_disc(turn, *move)
            self.assertEqual(move, expected)

    def test_neko_init(self):
        joseki = {}
        joseki.update(BULL)
        joseki.update(MOUSE)
        joseki.update(RABBIT)
        joseki.update(TIGER)
        joseki.update(SROSE)
        joseki.update(ROSEVILLE)
        joseki.update(FASTBOAT)
        joseki.update(SHEEP)
        joseki.update(CAT)

        # no Measure
        _neko_ = _Neko_(Random())
        key = _neko_.__class__.__name__ + str(os.getpid())
        board = BitBoard()
        _neko_.next_move(c.black, board)

        self.assertEqual(_neko_.joseki, joseki)
        self.assertIsInstance(_neko_.base, Random)
        self.assertFalse(key in Measure.elp_time)

        # with Measure
        neko = Neko(Random())
        key = neko.__class__.__name__ + str(os.getpid())
        board = BitBoard()
        neko.next_move(c.black, board)

        self.assertEqual(neko.joseki, joseki)
        self.assertIsInstance(neko.base, Random)
        self.assertTrue(key in Measure.elp_time)

    def test_neko_next_move(self):
        board = BitBoard()
        neko = Neko(Random())
        patterns = [
            # turn,   move
            # --- 猫定石 ---
            (c.black, (5, 4)),
            (c.white, (3, 5)),
            (c.black, (2, 3)),
            (c.white, (3, 2)),
            (c.black, (2, 4)),
            (c.white, (5, 3)),
            (c.black, (4, 2)),
            (c.white, (5, 2)),
            (c.black, (4, 1)),
            (c.white, (2, 5)),
            (c.black, (4, 5)),
            (c.white, (5, 5)),
            (c.black, (3, 6)),
            (c.white, (2, 7)),
        ]
        for turn, expected in patterns:
            move = neko.next_move(turn, board)
            board.put_disc(turn, *move)
            self.assertEqual(move, expected)
