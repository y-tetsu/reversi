"""Tests of easy.py
"""

import unittest

from reversi.board import Board
from reversi.strategies import Random, Greedy, Unselfish, SlowStarter


class TestEasy(unittest.TestCase):
    """easy
    """
    def test_random(self):
        random = Random()
        board = Board()

        legal_moves = list(board.get_legal_moves('black', board).keys())
        self.assertTrue(random.next_move('black', board) in legal_moves)

    def test_greedy(self):
        greedy = Greedy()
        board = Board()
        board.put_disc('black', 5, 4)
        board.put_disc('white', 3, 5)
        board.put_disc('black', 2, 4)
        board.put_disc('white', 5, 3)
        board.put_disc('black', 3, 6)
        board.put_disc('white', 6, 4)
        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 6)
        board.put_disc('black', 6, 3)
        board.put_disc('white', 3, 7)

        self.assertTrue(greedy.next_move('black', board) in [(7, 4), (1, 7)])

    def test_unselfish(self):
        unselfish = Unselfish()
        board = Board()
        board.put_disc('black', 5, 4)
        board.put_disc('white', 3, 5)
        board.put_disc('black', 2, 4)
        board.put_disc('white', 5, 3)
        board.put_disc('black', 3, 6)
        board.put_disc('white', 6, 4)
        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 6)
        board.put_disc('black', 6, 3)
        board.put_disc('white', 3, 7)

        self.assertTrue(unselfish.next_move('black', board) in [(7, 5), (4, 6)])

    def test_slowstarter(self):
        slowstarter = SlowStarter()
        board = Board()
        board.put_disc('black', 5, 4)  # 5
        board.put_disc('white', 3, 5)  # 6
        board.put_disc('black', 2, 4)  # 7
        board.put_disc('white', 5, 3)  # 8
        board.put_disc('black', 3, 6)  # 9

        # unselfish
        self.assertTrue(slowstarter.next_move('white', board) in [(6, 4), (1, 5), (2, 5), (5, 5), (6, 5), (2, 6)])

        board.put_disc('white', 6, 4)  # 10

        # greedy
        self.assertTrue(slowstarter.next_move('black', board) in [(7, 4)])
