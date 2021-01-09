"""Tests of custom.py
"""

import unittest

from reversi.strategies import MonteCarlo30, MonteCarlo100, MonteCarlo1000
from reversi.strategies import MinMax1_T, MinMax2_T, MinMax3_T, MinMax4_T
from reversi.strategies import MinMax1_TP, MinMax2_TP, MinMax3_TP, MinMax4_TP
from reversi.strategies import MinMax1_TPO, MinMax2_TPO, MinMax3_TPO, MinMax4_TPO
from reversi.strategies import MinMax1_TPW, MinMax2_TPW, MinMax3_TPW, MinMax4_TPW
from reversi.strategies import MinMax1_TPOW, MinMax2_TPOW, MinMax3_TPOW, MinMax4_TPOW
from reversi.strategies import MinMax1_TPWE, MinMax2_TPWE, MinMax3_TPWE, MinMax4_TPWE
from reversi.strategies import MinMax1_TPWEC, MinMax2_TPWEC, MinMax3_TPWEC, MinMax4_TPWEC
from reversi.strategies import MinMax1_PWE, MinMax2_PWE, MinMax3_PWE, MinMax4_PWE
from reversi.strategies import NegaMax1_TPW, NegaMax2_TPW, NegaMax3_TPW, NegaMax4_TPW
from reversi.strategies import NegaMax1_TPOW, NegaMax2_TPOW, NegaMax3_TPOW, NegaMax4_TPOW
from reversi.strategies import AlphaBeta1_TPW, AlphaBeta2_TPW, AlphaBeta3_TPW, AlphaBeta4_TPW
from reversi.strategies import AlphaBeta1_TPWE, AlphaBeta2_TPWE, AlphaBeta3_TPWE, AlphaBeta4_TPWE
from reversi.strategies import AlphaBeta_TPW, AlphaBeta_TPWE, AlphaBeta_TPWE_, AlphaBeta_TPWEC
from reversi.strategies.coordinator import Evaluator_T, Evaluator_TP, Evaluator_TPO, Evaluator_TPW, Evaluator_TPOW, Evaluator_TPWE, Evaluator_TPWEC, Evaluator_PWE  # noqa: E501


class TestCustom(unittest.TestCase):
    """custom
    """
    def test_montecarlo(self):
        patterns = [
            (MonteCarlo30(), 30),
            (MonteCarlo100(), 100),
            (MonteCarlo1000(), 1000),
        ]
        for obj, count in patterns:
            self.assertEqual(obj.count, count)

    def test_minmax(self):
        patterns = [
            ((MinMax1_T(), MinMax2_T(), MinMax3_T(), MinMax4_T()), Evaluator_T),
            ((MinMax1_TP(), MinMax2_TP(), MinMax3_TP(), MinMax4_TP()), Evaluator_TP),
            ((MinMax1_TPO(), MinMax2_TPO(), MinMax3_TPO(), MinMax4_TPO()), Evaluator_TPO),
            ((MinMax1_TPW(), MinMax2_TPW(), MinMax3_TPW(), MinMax4_TPW()), Evaluator_TPW),
            ((MinMax1_TPOW(), MinMax2_TPOW(), MinMax3_TPOW(), MinMax4_TPOW()), Evaluator_TPOW),
            ((MinMax1_TPWE(), MinMax2_TPWE(), MinMax3_TPWE(), MinMax4_TPWE()), Evaluator_TPWE),
            ((MinMax1_TPWEC(), MinMax2_TPWEC(), MinMax3_TPWEC(), MinMax4_TPWEC()), Evaluator_TPWEC),
            ((MinMax1_PWE(), MinMax2_PWE(), MinMax3_PWE(), MinMax4_PWE()), Evaluator_PWE),
        ]
        for strategies, evaluator in patterns:
            for depth, obj in enumerate(strategies, 1):
                self.assertEqual(obj.depth, depth)
                self.assertIsInstance(obj.evaluator, evaluator)

    def test_negamax(self):
        patterns = [
            ((NegaMax1_TPW(), NegaMax2_TPW(), NegaMax3_TPW(), NegaMax4_TPW()), Evaluator_TPW),
            ((NegaMax1_TPOW(), NegaMax2_TPOW(), NegaMax3_TPOW(), NegaMax4_TPOW()), Evaluator_TPOW),
        ]
        for strategies, evaluator in patterns:
            for depth, obj in enumerate(strategies, 1):
                self.assertEqual(obj.depth, depth)
                self.assertIsInstance(obj.evaluator, evaluator)

    def test_alphabeta(self):
        patterns = [
            ((AlphaBeta_TPW(),), Evaluator_TPW),
            ((AlphaBeta_TPWE(), AlphaBeta_TPWE_()), Evaluator_TPWE),
            ((AlphaBeta_TPWEC(),), Evaluator_TPWEC),
        ]
        for strategies, evaluator in patterns:
            for obj in strategies:
                self.assertIsInstance(obj.evaluator, evaluator)

        patterns = [
            ((AlphaBeta1_TPW(), AlphaBeta2_TPW(), AlphaBeta3_TPW(), AlphaBeta4_TPW()), Evaluator_TPW),
            ((AlphaBeta1_TPWE(), AlphaBeta2_TPWE(), AlphaBeta3_TPWE(), AlphaBeta4_TPWE()), Evaluator_TPWE),
        ]
        for strategies, evaluator in patterns:
            for depth, obj in enumerate(strategies, 1):
                self.assertEqual(obj.depth, depth)
                self.assertIsInstance(obj.evaluator, evaluator)
