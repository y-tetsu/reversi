"""Tests of sorter.py
"""

import unittest

from reversi.board import BitBoard
from reversi.strategies.coordinator import Sorter, Sorter_B, Sorter_C, Sorter_BC, Sorter_CB, Sorter_O


class TestSorter(unittest.TestCase):
    """sorter
    """
    def test_sorter(self):
        board = BitBoard(8)
        board.put_disc('black', 3, 2)
        sorter = Sorter()
        moves = sorter.sort_moves(color='white', board=board, moves=board.get_legal_moves('white'), best_move=None)

        self.assertEqual(moves, [(2, 2), (4, 2), (2, 4)])

    def test_sorter_b(self):
        board = BitBoard(8)
        board.put_disc('black', 3, 2)
        best_move = (4, 2)
        sorter = Sorter_B()
        moves = sorter.sort_moves(color='white', board=board, moves=board.get_legal_moves('white'), best_move=best_move)

        self.assertEqual(moves, [(4, 2), (2, 2), (2, 4)])

    def test_sorter_c(self):
        board = BitBoard(8)
        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 4)
        board.put_disc('black', 1, 5)
        board.put_disc('white', 1, 4)
        board.put_disc('black', 2, 5)
        board.put_disc('white', 2, 6)
        board.put_disc('black', 1, 6)
        board.put_disc('white', 1, 7)
        sorter = Sorter_C()
        moves = sorter.sort_moves(color='black', board=board, moves=board.get_legal_moves('black'), best_move=None)

        self.assertEqual(moves, [(0, 7), (0, 3), (2, 3), (0, 4), (5, 4), (0, 5), (4, 5), (5, 5), (0, 6), (2, 7)])

    def test_sorter_bc(self):
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
        sorter = Sorter_BC()
        moves = sorter.sort_moves(color='black', board=board, moves=board.get_legal_moves('black'), best_move=best_move)

        self.assertEqual(moves, [(0, 7), (2, 3), (0, 3), (0, 4), (5, 4), (0, 5), (4, 5), (5, 5), (0, 6), (2, 7)])

    def test_sorter_cb(self):
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
        sorter = Sorter_CB()
        moves = sorter.sort_moves(color='black', board=board, moves=board.get_legal_moves('black'), best_move=best_move)

        self.assertEqual(moves, [(2, 3), (0, 7), (0, 3), (0, 4), (5, 4), (0, 5), (4, 5), (5, 5), (0, 6), (2, 7)])

    def test_sorter_o(self):
        board = BitBoard(8)
        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 4)
        board.put_disc('black', 1, 5)
        board.put_disc('white', 1, 4)
        board.put_disc('black', 2, 5)
        board.put_disc('white', 2, 6)
        board.put_disc('black', 1, 6)
        board.put_disc('white', 1, 7)
        sorter = Sorter_O()
        moves = sorter.sort_moves(color='black', board=board, moves=board.get_legal_moves('black'), best_move=None)

        self.assertEqual(moves, [(2, 3), (0, 5), (0, 7), (2, 7), (0, 3), (5, 4), (4, 5), (5, 5), (0, 6), (0, 4)])
