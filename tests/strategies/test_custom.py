"""Tests of custom.py
"""

import unittest

from reversi.strategies import MonteCarlo30, MonteCarlo100, MonteCarlo1000
from reversi.strategies import MinMax1_T, MinMax2_T, MinMax3_T, MinMax4_T
from reversi.strategies import MinMax1_TP, MinMax2_TP, MinMax3_TP, MinMax4_TP
from reversi.strategies import MinMax1_TPO, MinMax2_TPO, MinMax3_TPO, MinMax4_TPO
from reversi.strategies.coordinator import Evaluator_T, Evaluator_TP, Evaluator_TPO


class TestCustom(unittest.TestCase):
    """custom
    """
    def test_montecarlo(self):
        patterns = [(MonteCarlo30(), 30), (MonteCarlo100(), 100), (MonteCarlo1000(), 1000)]
        for obj, count in patterns:
            self.assertEqual(obj.count, count)

    def test_minmax(self):
        patterns = [MinMax1_T(), MinMax2_T(), MinMax3_T(), MinMax4_T()]
        for depth, obj in enumerate(patterns, 1):
            self.assertEqual(obj.depth, depth)
            self.assertIsInstance(obj.evaluator, Evaluator_T)

        patterns = [MinMax1_TP(), MinMax2_TP(), MinMax3_TP(), MinMax4_TP()]
        for depth, obj in enumerate(patterns, 1):
            self.assertEqual(obj.depth, depth)
            self.assertIsInstance(obj.evaluator, Evaluator_TP)

        patterns = [MinMax1_TPO(), MinMax2_TPO(), MinMax3_TPO(), MinMax4_TPO()]
        for depth, obj in enumerate(patterns, 1):
            self.assertEqual(obj.depth, depth)
            self.assertIsInstance(obj.evaluator, Evaluator_TPO)
