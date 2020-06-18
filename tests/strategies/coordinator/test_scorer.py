"""Tests of display.py
"""

import unittest

from reversi.board import Board, BitBoard
from reversi.strategies.coordinator import TableScorer, PossibilityScorer


class TestScorer(unittest.TestCase):
    """scorer
    """
    def test_table_scorer(self):
        board = BitBoard()
        scorer = TableScorer()

        # initial value
        self.assertEqual(scorer.table.size, 8)
        self.assertEqual(scorer.table._CORNER, 50)
        self.assertEqual(scorer.table._C, -20)
        self.assertEqual(scorer.table._A1, 0)
        self.assertEqual(scorer.table._A2, -1)
        self.assertEqual(scorer.table._B, -1)
        self.assertEqual(scorer.table._X, -25)
        self.assertEqual(scorer.table._O, -5)
        self.assertEqual(scorer.get_score('black', board), 0)
        self.assertEqual(scorer.get_score('white', board), 0)

        # b
        board.put_disc('black', 5, 4)
        self.assertEqual(scorer.get_score('black', board), -3)
        self.assertEqual(scorer.get_score('white', board), -3)

        # a1
        board.put_disc('white', 5, 5)
        self.assertEqual(scorer.get_score('black', board), -1)
        self.assertEqual(scorer.get_score('white', board), -1)

        # o
        board.put_disc('black', 5, 6)
        self.assertEqual(scorer.get_score('black', board), -6)
        self.assertEqual(scorer.get_score('white', board), -6)

        # x
        board.put_disc('white', 6, 6)
        self.assertEqual(scorer.get_score('black', board), 19)
        self.assertEqual(scorer.get_score('white', board), 19)

        # c
        board.put_disc('black', 7, 6)
        self.assertEqual(scorer.get_score('black', board), -51)
        self.assertEqual(scorer.get_score('white', board), -51)

        # corner
        board.put_disc('white', 7, 7)
        self.assertEqual(scorer.get_score('black', board), -51)
        self.assertEqual(scorer.get_score('white', board), -51)

        # a2
        board.put_disc('white', 5, 7)
        self.assertEqual(scorer.get_score('black', board), -40)
        self.assertEqual(scorer.get_score('white', board), -40)

    def test_possibility_scorer(self):
        board = Board()
        scorer = PossibilityScorer()

        # initial value
        self.assertEqual(scorer._W, 5)
        black_moves = board.get_legal_moves('black', force=True)
        white_moves = board.get_legal_moves('white', force=True)
        self.assertEqual(scorer.get_score(black_moves, white_moves), 0)

        board.put_disc('black', 5, 4)
        print(board)

        black_moves = board.get_legal_moves('black', force=True)
        white_moves = board.get_legal_moves('white', force=True)
        print('black', black_moves)
        print('white', white_moves)
        self.assertEqual(scorer.get_score(black_moves, white_moves), 0)

