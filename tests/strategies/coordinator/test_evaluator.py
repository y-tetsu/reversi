"""Tests of evaluator.py
"""

import unittest

from reversi.board import Board, BitBoard
from reversi.strategies.coordinator import Evaluator_T, Evaluator_TP, Evaluator_TPO, Evaluator_TPOW, Evaluator_PW, Evaluator_N, Evaluator_NW, Evaluator_TPWE, Evaluator_TPWEC, Evaluator_PWE


class TestEvaluator(unittest.TestCase):
    """evaluator
    """
    def test_customized_evaluator(self):
        board8 = BitBoard(8)
        board8.put_disc('black', 3, 2)
        board8.put_disc('white', 2, 2)
        board8.put_disc('black', 2, 3)
        board8.put_disc('white', 4, 2)
        board8.put_disc('black', 1, 1)
        board8.put_disc('white', 0, 0)

        legal_moves_b = board8.get_legal_moves('black', force=True)
        legal_moves_w = board8.get_legal_moves('white', force=True)

        # Evaluator_T
        evaluator = Evaluator_T()
        score_b = evaluator.evaluate(color='black', board=board8)
        score_w = evaluator.evaluate(color='white', board=board8)
        self.assertEqual(score_b, -22)
        self.assertEqual(score_w, -22)

        # Evaluator_TP
        evaluator = Evaluator_TP()
        score_b = evaluator.evaluate(color='black', board=board8, legal_moves_b=legal_moves_b, legal_moves_w=legal_moves_w)
        self.assertEqual(score_b, -17)

        # Evaluator_TPO
        evaluator = Evaluator_TPO()
        score_b = evaluator.evaluate(color='black', board=board8, legal_moves_b=legal_moves_b, legal_moves_w=legal_moves_w)
        self.assertEqual(score_b, -25.25)

        # Evaluator_TPOW
        evaluator = Evaluator_TPOW()
        score_b = evaluator.evaluate(color='black', board=board8, legal_moves_b=[], legal_moves_w=[])
        self.assertEqual(score_b, -10006)
        score_b = evaluator.evaluate(color='black', board=board8, legal_moves_b=legal_moves_b, legal_moves_w=legal_moves_w)
        self.assertEqual(score_b, -25.25)

        # Evaluator_PW
        evaluator = Evaluator_PW()
        score = evaluator.evaluate(board=board8, legal_moves_b=[], legal_moves_w=[])
        self.assertEqual(score, -10006)
        score = evaluator.evaluate(board=board8, legal_moves_b=legal_moves_b, legal_moves_w=legal_moves_w)
        self.assertEqual(score, 5)

        # Evaluator_N
        evaluator = Evaluator_N()
        score_b = evaluator.evaluate(color='black', board=board8, legal_moves_b=[], legal_moves_w=[])
        self.assertEqual(score_b, -6)

        # Evaluator_NW
        evaluator = Evaluator_NW()
        score = evaluator.evaluate(board=board8, legal_moves_b=[], legal_moves_w=[])
        self.assertEqual(score, -10006)
        score = evaluator.evaluate(board=board8, legal_moves_b=legal_moves_b, legal_moves_w=legal_moves_w)
        self.assertEqual(score, -6)

        # Evaluator_TPWE
        evaluator = Evaluator_TPWE()
        board8._black_bitboard = 0x0000002010003C7E
        legal_moves_b = board8.get_legal_moves('black', True)
        legal_moves_w = board8.get_legal_moves('white', True)
        score = evaluator.evaluate(color='black', board=board8, legal_moves_b=legal_moves_b, legal_moves_w=legal_moves_w)
        self.assertEqual(score, -81)

        board8._black_bitboard = 0x0000002010003C7C
        score = evaluator.evaluate(color='black', board=board8, legal_moves_b=legal_moves_b, legal_moves_w=legal_moves_w)
        self.assertEqual(score, -61)

        # Evaluator_TPWEC
        evaluator = Evaluator_TPWEC()
        board8._black_bitboard = 0x0000002010003C7C
        legal_moves_b = board8.get_legal_moves('black', True)
        legal_moves_w = board8.get_legal_moves('white', True)
        score = evaluator.evaluate(color='black', board=board8, legal_moves_b=legal_moves_b, legal_moves_w=legal_moves_w)
        self.assertEqual(score, -61)
        board8._black_bitboard = 0x0703012010003C7E
        score = evaluator.evaluate(color='black', board=board8, legal_moves_b=legal_moves_b, legal_moves_w=legal_moves_w)
        self.assertEqual(score, 422)

        # Evaluator_PWE
        evaluator = Evaluator_PWE()
        board8._black_bitboard = 0x0000002010003C7C
        legal_moves_b = board8.get_legal_moves('black', True)
        legal_moves_w = board8.get_legal_moves('white', True)
        score = evaluator.evaluate(color='black', board=board8, legal_moves_b=legal_moves_b, legal_moves_w=legal_moves_w)
        self.assertEqual(score, 10)
        board8._black_bitboard = 0x0703012010003C7E
        score = evaluator.evaluate(color='black', board=board8, legal_moves_b=legal_moves_b, legal_moves_w=legal_moves_w)
        self.assertEqual(score, 310)
