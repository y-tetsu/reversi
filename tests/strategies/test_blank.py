"""Tests of blank.py
"""

import unittest
import os
import time

from reversi.board import BitBoard
from reversi.strategies.common import Timer, Measure, CPU_TIME
from reversi.strategies import _Blank_, _Blank, Blank_, Blank, _NegaScout_, _NegaScout, NegaScout_, NegaScout
import reversi.strategies.coordinator as coord


class TestBlank(unittest.TestCase):
    """blank
    """
    def test_blank_init(self):
        negascout_tpweb = [_NegaScout_, _NegaScout, NegaScout_, NegaScout]
        timer = [False, False, True, True]
        measure = [False, True, False, True]
        for index, instance in enumerate([_Blank_, _Blank, Blank_, Blank]):
            blank = instance()
            self.assertEqual(blank._MIN, -10000000)
            self.assertEqual(blank._MAX, 10000000)
            self.assertTrue(isinstance(blank.evaluator, coord.Evaluator_TPWEB))
            self.assertEqual(blank.depth, 4)
            self.assertTrue(isinstance(blank.negascout_tpweb, negascout_tpweb[index]))
            self.assertEqual(blank.timer, timer[index])
            self.assertEqual(blank.measure, measure[index])
        depth = 12
        for index, instance in enumerate([_Blank_, _Blank, Blank_, Blank]):
            blank = instance(depth)
            self.assertEqual(blank._MIN, -10000000)
            self.assertEqual(blank._MAX, 10000000)
            self.assertTrue(isinstance(blank.evaluator, coord.Evaluator_TPWEB))
            self.assertEqual(blank.depth, depth)
            self.assertTrue(isinstance(blank.negascout_tpweb, negascout_tpweb[index]))
            self.assertEqual(blank.timer, timer[index])
            self.assertEqual(blank.measure, measure[index])

    def test_blank_next_move(self):
        expected = _NegaScout_(depth=4, evaluator=coord.Evaluator_TPWEB())
        for instance in [_Blank_, _Blank, Blank_, Blank]:
            board = BitBoard()
            blank = instance(depth=4)

            board.put_disc('black', 3, 2)
            self.assertEqual(blank.next_move('white', board), expected.next_move('white', board))

            board.put_disc('white', 2, 4)
            board.put_disc('black', 5, 5)
            board.put_disc('white', 4, 2)
            board.put_disc('black', 5, 2)
            board.put_disc('white', 5, 4)
            self.assertEqual(blank.next_move('black', board), expected.next_move('black', board))

            board.put_disc('black', 2, 3)
            board.put_disc('white', 1, 2)
            board.put_disc('black', 5, 3)
            board.put_disc('white', 2, 2)
            board.put_disc('black', 4, 5)
            self.assertEqual(blank.next_move('white', board), expected.next_move('white', board))
