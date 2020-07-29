"""Tests of selector.py
"""

import unittest

from reversi.board import BitBoard
from reversi.strategies.alphabeta import _AlphaBeta
from reversi.strategies.coordinator import Selector, Selector_W, Evaluator_TPW


class TestSelector(unittest.TestCase):
    """selector
    """
    def test_selector(self):
        board = BitBoard(8)
        board.put_disc('black', 3, 2)
        selector = Selector()
        moves = selector.select_moves('white', board, board.get_legal_moves('white'), None, None)

        self.assertEqual(moves, [(2, 2), (4, 2), (2, 4)])

    def test_selector_w(self):
        board = BitBoard(8)
        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 4)
        board.put_disc('black', 1, 5)
        board.put_disc('white', 1, 4)
        board.put_disc('black', 2, 5)
        board.put_disc('white', 2, 6)
        board.put_disc('black', 1, 6)
        board.put_disc('white', 1, 7)
        selector = Selector_W(depth=2, limit=4)

        self.assertEqual(selector.depth, 2)
        self.assertEqual(selector.limit, 4)

        strategy = _AlphaBeta(evaluator=Evaluator_TPW())
        selector = Selector_W()

        self.assertEqual(selector.depth, 3)
        self.assertEqual(selector.limit, 3)

        moves = board.get_legal_moves('black')
        best_move, scores = strategy.get_best_move('black', board, moves, 4)
        moves = selector.select_moves('black', board, board.get_legal_moves('black'), scores, 2)
        self.assertEqual(moves, [(0, 3), (2, 3), (0, 4), (5, 4), (0, 5), (4, 5), (5, 5), (0, 6), (0, 7), (2, 7)])

        moves = selector.select_moves('black', board, board.get_legal_moves('black'), scores, 5)
        self.assertEqual(moves, [(2, 3), (0, 4), (5, 4), (0, 5), (4, 5), (5, 5), (0, 6), (0, 7), (2, 7)])
