"""Tests of measure.py
"""

import unittest
import os
import time

from reversi import BitBoard
from reversi import C as c
from reversi.strategies import AbstractStrategy
from reversi.strategies.common import Measure


class TestMeasure(unittest.TestCase):
    """measure
    """
    def test_measure_time(self):
        repeat = 10
        wait = 0.01

        class TestTime(AbstractStrategy):
            @Measure.time
            def next_move(self, color, board):
                time.sleep(wait)
                return (0, 0)

        pid = "TestTime" + str(os.getpid())
        self.assertTrue(pid not in Measure.elp_time)

        strategy = TestTime()
        for _ in range(repeat):
            board = BitBoard()
            strategy.next_move(c.black, board)

        self.assertTrue(pid in Measure.elp_time)
        self.assertEqual(Measure.elp_time[pid]['cnt'], repeat)
        self.assertGreaterEqual(Measure.elp_time[pid]['max'], Measure.elp_time[pid]['ave'])
        self.assertGreaterEqual(Measure.elp_time[pid]['ave'], Measure.elp_time[pid]['min'])

    def test_measure_countup(self):
        repeat = 10

        class TestCountup():
            @Measure.countup
            def countup_method(self, pid=None):
                pass

        pid = "TestCountup" + str(os.getpid())
        self.assertTrue(pid not in Measure.count)

        strategy = TestCountup()
        for _ in range(repeat):
            strategy.countup_method(pid=pid)

        self.assertTrue(pid in Measure.count)
        self.assertEqual(Measure.count[pid], repeat)
