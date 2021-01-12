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
from reversi.strategies import AlphaBeta_TPW, AlphaBeta_TPWE, AlphaBeta_TPWE_, AlphaBeta_TPWEC
from reversi.strategies import AlphaBeta1_TPW, AlphaBeta2_TPW, AlphaBeta3_TPW, AlphaBeta4_TPW
from reversi.strategies import AlphaBeta1_TPWE, AlphaBeta2_TPWE, AlphaBeta3_TPWE, AlphaBeta4_TPWE
from reversi.strategies import NegaScout_TPW, NegaScout_TPWE
from reversi.strategies import NegaScout1_TPW, NegaScout2_TPW, NegaScout3_TPW, NegaScout4_TPW
from reversi.strategies import NegaScout1_TPOW, NegaScout2_TPOW, NegaScout3_TPOW, NegaScout4_TPOW
from reversi.strategies import NegaScout1_TPWE, NegaScout2_TPWE, NegaScout3_TPWE, NegaScout4_TPWE
from reversi.strategies import AbI_B_TPW, AbI_B_TPWE, AbI_PCB_TPWE, _AbI_B_TPWE_, AbI_B_TPWEC, NsI_B_TPW, NsI_B_TPWE
from reversi.strategies.coordinator import Evaluator_T, Evaluator_TP, Evaluator_TPO, Evaluator_TPW, Evaluator_TPOW, Evaluator_TPWE, Evaluator_TPWEC, Evaluator_PWE  # noqa: E501
from reversi.strategies.coordinator import Selector
from reversi.strategies.coordinator import Orderer_B, Orderer_PCB


class TestCustom(unittest.TestCase):
    """custom
    """
    def test_custom_montecarlo(self):
        patterns = [
            (MonteCarlo30(), 30),
            (MonteCarlo100(), 100),
            (MonteCarlo1000(), 1000),
        ]
        for obj, count in patterns:
            self.assertEqual(obj.count, count)

    def test_custom_minmax(self):
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

    def test_custom_negamax(self):
        patterns = [
            ((NegaMax1_TPW(), NegaMax2_TPW(), NegaMax3_TPW(), NegaMax4_TPW()), Evaluator_TPW),
            ((NegaMax1_TPOW(), NegaMax2_TPOW(), NegaMax3_TPOW(), NegaMax4_TPOW()), Evaluator_TPOW),
        ]
        for strategies, evaluator in patterns:
            for depth, obj in enumerate(strategies, 1):
                self.assertEqual(obj.depth, depth)
                self.assertIsInstance(obj.evaluator, evaluator)

    def test_custom_alphabeta(self):
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

    def test_custom_negascout(self):
        patterns = [
            ((NegaScout_TPW(),), Evaluator_TPW),
            ((NegaScout_TPWE(),), Evaluator_TPWE),
        ]
        for strategies, evaluator in patterns:
            for obj in strategies:
                self.assertIsInstance(obj.evaluator, evaluator)

        patterns = [
            ((NegaScout1_TPW(), NegaScout2_TPW(), NegaScout3_TPW(), NegaScout4_TPW()), Evaluator_TPW),
            ((NegaScout1_TPOW(), NegaScout2_TPOW(), NegaScout3_TPOW(), NegaScout4_TPOW()), Evaluator_TPOW),
            ((NegaScout1_TPWE(), NegaScout2_TPWE(), NegaScout3_TPWE(), NegaScout4_TPWE()), Evaluator_TPWE),
        ]
        for strategies, evaluator in patterns:
            for depth, obj in enumerate(strategies, 1):
                self.assertEqual(obj.depth, depth)
                self.assertIsInstance(obj.evaluator, evaluator)

    def test_custom_iterative(self):
        patterns = [
            (AbI_B_TPW(),    2, Selector, Orderer_B,   AlphaBeta_TPW),
            (AbI_B_TPWE(),   2, Selector, Orderer_B,   AlphaBeta_TPWE),
            (AbI_PCB_TPWE(), 2, Selector, Orderer_PCB, AlphaBeta_TPWE),
            (_AbI_B_TPWE_(), 2, Selector, Orderer_B,   AlphaBeta_TPWE_),
            (AbI_B_TPWEC(),  2, Selector, Orderer_B,   AlphaBeta_TPWEC),
            (NsI_B_TPW(),    2, Selector, Orderer_B,   NegaScout_TPW),
            (NsI_B_TPWE(),   2, Selector, Orderer_B,   NegaScout_TPWE),
        ]
        for obj, depth, selector, orderer, search in patterns:
            self.assertEqual(obj.depth, depth)
            self.assertIsInstance(obj.selector, selector)
            self.assertIsInstance(obj.orderer, orderer)
            self.assertIsInstance(obj.search, search)
