"""Tests of orderer.py
"""

import unittest

from reversi.board import BitBoard
from reversi.strategies.coordinator import Orderer, Orderer_B, Orderer_C, Orderer_BC, Orderer_CB


class TestOrderer(unittest.TestCase):
    """orderer
    """
    def test_orderer(self):
        board = BitBoard(8)
        board.put_disc('black', 3, 2)
        orderer = Orderer()
        moves = orderer.move_ordering(color='white', board=board, moves=board.get_legal_moves('white'), best_move=None)

        self.assertEqual(moves, [(2, 2), (4, 2), (2, 4)])

    def test_orderer_b(self):
        board = BitBoard(8)
        board.put_disc('black', 3, 2)
        best_move = (4, 2)
        orderer = Orderer_B()
        moves = orderer.move_ordering(color='white', board=board, moves=board.get_legal_moves('white'), best_move=best_move)

        self.assertEqual(moves, [(4, 2), (2, 2), (2, 4)])

    def test_orderer_c(self):
        board = BitBoard(8)
        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 4)
        board.put_disc('black', 1, 5)
        board.put_disc('white', 1, 4)
        board.put_disc('black', 2, 5)
        board.put_disc('white', 2, 6)
        board.put_disc('black', 1, 6)
        board.put_disc('white', 1, 7)
        orderer = Orderer_C()
        moves = orderer.move_ordering(color='black', board=board, moves=board.get_legal_moves('black'), best_move=None)

        self.assertEqual(moves, [(0, 7), (0, 3), (2, 3), (0, 4), (5, 4), (0, 5), (4, 5), (5, 5), (0, 6), (2, 7)])

    def test_orderer_bc(self):
        board = BitBoard(8)
        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 4)
        board.put_disc('black', 1, 5)
        board.put_disc('white', 1, 4)
        board.put_disc('black', 2, 5)
        board.put_disc('white', 2, 6)
        board.put_disc('black', 1, 6)
        board.put_disc('white', 1, 7)
        best_move = (2, 3)
        orderer = Orderer_BC()
        moves = orderer.move_ordering(color='black', board=board, moves=board.get_legal_moves('black'), best_move=best_move)

        self.assertEqual(moves, [(0, 7), (2, 3), (0, 3), (0, 4), (5, 4), (0, 5), (4, 5), (5, 5), (0, 6), (2, 7)])

    def test_orderer_cb(self):
        board = BitBoard(8)
        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 4)
        board.put_disc('black', 1, 5)
        board.put_disc('white', 1, 4)
        board.put_disc('black', 2, 5)
        board.put_disc('white', 2, 6)
        board.put_disc('black', 1, 6)
        board.put_disc('white', 1, 7)
        best_move = (2, 3)
        orderer = Orderer_CB()
        moves = orderer.move_ordering(color='black', board=board, moves=board.get_legal_moves('black'), best_move=best_move)

        self.assertEqual(moves, [(2, 3), (0, 7), (0, 3), (0, 4), (5, 4), (0, 5), (4, 5), (5, 5), (0, 6), (2, 7)])
