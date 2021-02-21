"""Tests of custom.py
"""

import unittest

from reversi import BitBoard, C as c
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
from reversi.strategies import AbI_B_TPW, AbI_B_TPWE, AbI_PCB_TPWE, AbI_B_TPWE_, AbI_B_TPWEC, NsI_B_TPW, NsI_B_TPWE
from reversi.strategies import IterativeDeepning
from reversi.strategies import AlphaBeta, NegaScout
from reversi.strategies import SwitchAbI_B_TPWE, SwitchNsI_B_TPWE, SwitchNsI_B_TPWE_Type2
from reversi.strategies import Random
from reversi.strategies import MinMax2F9_TPWE, AlphaBeta4F9_TPW, AlphaBeta4F10_TPW, AbIF9_B_TPW, AbIF9_B_TPWE, AbIF9_PCB_TPWE, AbIF10_B_TPWE, AbIF10_PCB_TPWE, AbIF9_B_TPWE_, AbIF9_B_TPWEC, NsIF9_B_TPW, NsIF9_B_TPWE, NsIF10_B_TPWE, NsIF10_B_TPW, NsIF11_B_TPW, NsIF12_B_TPW, SwitchAbIF9_B_TPWE, SwitchNsIF9_B_TPWE, SwitchNsIF10_B_TPWE, SwitchNsIF10_B_TPWE_Type2, RandomF11  # noqa: E501
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
            (AbI_B_TPWE_(),  2, Selector, Orderer_B,   AlphaBeta_TPWE_),
            (AbI_B_TPWEC(),  2, Selector, Orderer_B,   AlphaBeta_TPWEC),
            (NsI_B_TPW(),    2, Selector, Orderer_B,   NegaScout_TPW),
            (NsI_B_TPWE(),   2, Selector, Orderer_B,   NegaScout_TPWE),
        ]
        for obj, depth, selector, orderer, search in patterns:
            self.assertEqual(obj.depth, depth)
            self.assertIsInstance(obj.selector, selector)
            self.assertIsInstance(obj.orderer, orderer)
            self.assertIsInstance(obj.search, search)

    def test_custom_switch(self):
        patterns = [
            (
                SwitchAbI_B_TPWE(),
                [12, 24, 36, 48, 60],
                [
                    (IterativeDeepning, 2, Selector, Orderer_B, AlphaBeta, Evaluator_TPWE, 50, -20, -10,  0, -4, -2, -2, -25, -13, -5, 4,  9999,  91),
                    (IterativeDeepning, 2, Selector, Orderer_B, AlphaBeta, Evaluator_TPWE, 44, -18,  -4, -2, -2, -4, -3, -40, -10, -8, 4, 10001,  95),
                    (IterativeDeepning, 2, Selector, Orderer_B, AlphaBeta, Evaluator_TPWE, 41, -14,  -1, -4, -4, -1,  2, -38,  -5, -5, 4,  9996, 103),
                    (IterativeDeepning, 2, Selector, Orderer_B, AlphaBeta, Evaluator_TPWE, 62, -19,   1,  0, -1,  0,  1, -25,  -4, -2, 8,  9990,  94),
                    (IterativeDeepning, 2, Selector, Orderer_B, AlphaBeta, Evaluator_TPWE, 50, -23,   0, -9, -2, -2, 16, -25,  -9, -8, 8,  9998,  93),
                ],
            ),
            (
                SwitchNsI_B_TPWE(),
                [12, 24, 36, 48, 60],
                [
                    (IterativeDeepning, 2, Selector, Orderer_B, NegaScout, Evaluator_TPWE, 50, -20, -10,  0, -4, -2, -2, -25, -13, -5, 4,  9999,  91),
                    (IterativeDeepning, 2, Selector, Orderer_B, NegaScout, Evaluator_TPWE, 44, -18,  -4, -2, -2, -4, -3, -40, -10, -8, 4, 10001,  95),
                    (IterativeDeepning, 2, Selector, Orderer_B, NegaScout, Evaluator_TPWE, 41, -14,  -1, -4, -4, -1,  2, -38,  -5, -5, 4,  9996, 103),
                    (IterativeDeepning, 2, Selector, Orderer_B, NegaScout, Evaluator_TPWE, 62, -19,   1,  0, -1,  0,  1, -25,  -4, -2, 8,  9990,  94),
                    (IterativeDeepning, 2, Selector, Orderer_B, NegaScout, Evaluator_TPWE, 50, -23,   0, -9, -2, -2, 16, -25,  -9, -8, 8,  9998,  93),
                ],
            ),
            (
                SwitchNsI_B_TPWE_Type2(),
                [12, 24, 36, 48, 60],
                [
                    (IterativeDeepning, 2, Selector, Orderer_B, NegaScout, Evaluator_TPWE, 42, -17,  -7,   2, -7, -6, -3, -26, -23,  -9,  4, 10002,  84),
                    (IterativeDeepning, 2, Selector, Orderer_B, NegaScout, Evaluator_TPWE, 39, -12,  -3,  -3, -5, -4, -2, -34,  -9,  -7,  4, 10003,  82),
                    (IterativeDeepning, 2, Selector, Orderer_B, NegaScout, Evaluator_TPWE, 43, -20,  -2,  -2, -2, -2,  3, -32,  -4,  -6,  4,  9996, 114),
                    (IterativeDeepning, 2, Selector, Orderer_B, NegaScout, Evaluator_TPWE, 67, -19,  -6,   1, -1,  0,  3, -24,  -5,  -2, 10,  9993, 101),
                    (IterativeDeepning, 2, Selector, Orderer_B, NegaScout, Evaluator_TPWE, 47, -37, -11, -15,  5, -3, 16, -24,  -6, -15, 12,  9999,  87),
                ],
            ),
        ]
        for obj, turns, strategies in patterns:
            self.assertEqual(obj.turns, turns)
            self.assertEqual(len(obj.strategies), len(strategies))
            for index, strategy in enumerate(obj.strategies):
                self.assertIsInstance(strategy, strategies[index][0])
                self.assertEqual(strategy.depth, strategies[index][1])
                self.assertIsInstance(strategy.selector, strategies[index][2])
                self.assertIsInstance(strategy.orderer, strategies[index][3])
                self.assertIsInstance(strategy.search, strategies[index][4])
                self.assertIsInstance(strategy.search.evaluator, strategies[index][5])
                self.assertEqual(strategy.search.evaluator.t.table._CORNER, strategies[index][6])
                self.assertEqual(strategy.search.evaluator.t.table._C, strategies[index][7])
                self.assertEqual(strategy.search.evaluator.t.table._A1, strategies[index][8])
                self.assertEqual(strategy.search.evaluator.t.table._A2, strategies[index][9])
                self.assertEqual(strategy.search.evaluator.t.table._B1, strategies[index][10])
                self.assertEqual(strategy.search.evaluator.t.table._B2, strategies[index][11])
                self.assertEqual(strategy.search.evaluator.t.table._B3, strategies[index][12])
                self.assertEqual(strategy.search.evaluator.t.table._X, strategies[index][13])
                self.assertEqual(strategy.search.evaluator.t.table._O1, strategies[index][14])
                self.assertEqual(strategy.search.evaluator.t.table._O2, strategies[index][15])
                self.assertEqual(strategy.search.evaluator.p._W, strategies[index][16])
                self.assertEqual(strategy.search.evaluator.w._W, strategies[index][17])
                self.assertEqual(strategy.search.evaluator.e._W, strategies[index][18])

    def test_custom_fullreading(self):
        patterns = [
            (MinMax2F9_TPWE(),             9, MinMax2_TPWE),
            (AlphaBeta4F9_TPW(),           9, AlphaBeta4_TPW),
            (AlphaBeta4F10_TPW(),         10, AlphaBeta4_TPW),
            (AbIF9_B_TPW(),                9, AbI_B_TPW),
            (AbIF9_B_TPWE(),               9, AbI_B_TPWE),
            (AbIF9_PCB_TPWE(),             9, AbI_PCB_TPWE),
            (AbIF10_B_TPWE(),             10, AbI_B_TPWE),
            (AbIF10_PCB_TPWE(),           10, AbI_PCB_TPWE),
            (AbIF9_B_TPWE_(),              9, AbI_B_TPWE_),
            (AbIF9_B_TPWEC(),              9, AbI_B_TPWEC),
            (NsIF9_B_TPW(),                9, NsI_B_TPW),
            (NsIF9_B_TPWE(),               9, NsI_B_TPWE),
            (NsIF10_B_TPWE(),             10, NsI_B_TPWE),
            (NsIF10_B_TPW(),              10, NsI_B_TPW),
            (NsIF11_B_TPW(),              11, NsI_B_TPW),
            (NsIF12_B_TPW(),              12, NsI_B_TPW),
            (SwitchAbIF9_B_TPWE(),         9, SwitchAbI_B_TPWE),
            (SwitchNsIF9_B_TPWE(),         9, SwitchNsI_B_TPWE),
            (SwitchNsIF10_B_TPWE(),       10, SwitchNsI_B_TPWE),
            (SwitchNsIF10_B_TPWE_Type2(), 10, SwitchNsI_B_TPWE_Type2),
            (RandomF11(),                 11, Random),
        ]
        for obj, remain, base in patterns:
            self.assertEqual(obj.remain, remain)
            self.assertIsInstance(obj.base, base)

        randomf11 = RandomF11()
        board = BitBoard(4)
        moves_size4 = [(1, 0), (0, 1), (3, 2), (2, 3)]
        self.assertTrue(randomf11.next_move(c.black, board) in moves_size4)

        board = BitBoard(6)
        moves_size6 = [(2, 1), (1, 2), (4, 3), (3, 4)]
        self.assertTrue(randomf11.next_move(c.black, board) in moves_size6)
