"""Tests of proto.py
"""

import unittest
import os
import time

from reversi.board import BitBoard
from reversi.strategies.common import Timer, Measure, CPU_TIME
from reversi.strategies import MinMax2, NegaMax3, AlphaBeta4, AB_T4, AB_TI


class TestAlphaBeta(unittest.TestCase):
    """alphabeta
    """
    def test_proto_minmax2_init(self):
        minmax2 = MinMax2()

        self.assertEqual(minmax2._W1, 10000)
        self.assertEqual(minmax2._W2, 16)
        self.assertEqual(minmax2._W3, 2)
        self.assertEqual(minmax2._MIN, -10000000)
        self.assertEqual(minmax2._MAX, 10000000)
        self.assertEqual(minmax2.depth, 2)

    def test_proto_minmax2_next_move(self):
        minmax2 = MinMax2()
        board = BitBoard()

        board.put_disc('black', 3, 2)
        self.assertEqual(minmax2.next_move('white', board), (2, 4))

        board.put_disc('white', 2, 4)
        board.put_disc('black', 1, 5)
        board.put_disc('white', 1, 4)
        self.assertEqual(minmax2.next_move('black', board), (2, 5))

    def test_proto_minmax2_get_score(self):
        minmax2 = MinMax2()
        board = BitBoard(4)
        board._black_bitboard = 0x0400
        board._white_bitboard = 0x8030

        self.assertEqual(minmax2.get_score('white', board, 2), 2)

    def test_proto_minmax2_evaluate(self):
        minmax2 = MinMax2()
        board = BitBoard(4)

        self.assertEqual(minmax2.evaluate(board, [], []), 0)

        board._black_score = 3
        self.assertEqual(minmax2.evaluate(board, [], []), 10001)

        board._white_score = 4
        self.assertEqual(minmax2.evaluate(board, [], []), -10001)

    def test_proto_negamax3_init(self):
        negamax3 = NegaMax3()

        self.assertEqual(negamax3._W1, 10000)
        self.assertEqual(negamax3._W2, 16)
        self.assertEqual(negamax3._W3, 2)
        self.assertEqual(negamax3._MIN, -10000000)
        self.assertEqual(negamax3._MAX, 10000000)
        self.assertEqual(negamax3.depth, 3)

    def test_proto_alphabeta4_init(self):
        alphabeta4 = AlphaBeta4()

        self.assertEqual(alphabeta4._W1, 10000)
        self.assertEqual(alphabeta4._W2, 16)
        self.assertEqual(alphabeta4._W3, 2)
        self.assertEqual(alphabeta4._MIN, -10000000)
        self.assertEqual(alphabeta4._MAX, 10000000)
        self.assertEqual(alphabeta4.depth, 4)

    def test_proto_ab_t4_init(self):
        ab_t4 = AB_T4()

        self.assertEqual(ab_t4._W1, 10000)
        self.assertEqual(ab_t4._W2, 16)
        self.assertEqual(ab_t4._W3, 2)
        self.assertEqual(ab_t4._MIN, -10000000)
        self.assertEqual(ab_t4._MAX, 10000000)
        self.assertEqual(ab_t4.depth, 4)
        self.assertEqual(ab_t4.table.size, 8)
        self.assertEqual(ab_t4.table._CORNER, 50)
        self.assertEqual(ab_t4.table._C, -20)
        self.assertEqual(ab_t4.table._A1, 0)
        self.assertEqual(ab_t4.table._A2, 0)
        self.assertEqual(ab_t4.table._B1, -1)
        self.assertEqual(ab_t4.table._B2, -1)
        self.assertEqual(ab_t4.table._B3, -1)
        self.assertEqual(ab_t4.table._X, -25)
        self.assertEqual(ab_t4.table._O1, -5)
        self.assertEqual(ab_t4.table._O2, -5)
        self.assertEqual(ab_t4._W4, 0.5)

    def test_proto_ab_ti_init(self):
        ab_ti = AB_TI()

        self.assertEqual(ab_ti._W1, 10000)
        self.assertEqual(ab_ti._W2, 16)
        self.assertEqual(ab_ti._W3, 2)
        self.assertEqual(ab_ti._MIN, -10000000)
        self.assertEqual(ab_ti._MAX, 10000000)
        self.assertEqual(ab_ti.depth, 2)
        self.assertEqual(ab_ti.table.size, 8)
        self.assertEqual(ab_ti.table._CORNER, 50)
        self.assertEqual(ab_ti.table._C, -20)
        self.assertEqual(ab_ti.table._A1, 0)
        self.assertEqual(ab_ti.table._A2, 0)
        self.assertEqual(ab_ti.table._B1, -1)
        self.assertEqual(ab_ti.table._B2, -1)
        self.assertEqual(ab_ti.table._B3, -1)
        self.assertEqual(ab_ti.table._X, -25)
        self.assertEqual(ab_ti.table._O1, -5)
        self.assertEqual(ab_ti.table._O2, -5)
        self.assertEqual(ab_ti._W4, 0.5)
