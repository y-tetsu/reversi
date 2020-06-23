"""Tests of table.py
"""

import unittest

from reversi.board import Board
from reversi.strategies import Table


class TestTable(unittest.TestCase):
    """scorer
    """
    def test_table_init(self):
        table = Table(4)
        init = [
            [0, -1, -1, 0],
            [-1, -1, -1, -1],
            [-1, -1, -1, -1],
            [0, -1, -1, 0],
        ]

        self.assertEqual(table.table, init)

        table = Table(8)
        init = [
            [ 50, -20, -1, -1, -1, -1, -20,  50],
            [-20, -25, -5, -5, -5, -5, -25, -20],
            [ -1,  -5,  0, -1, -1,  0,  -5,  -1],
            [ -1,  -5, -1, -1, -1, -1,  -5,  -1],
            [ -1,  -5, -1, -1, -1, -1,  -5,  -1],
            [ -1,  -5,  0, -1, -1,  0,  -5,  -1],
            [-20, -25, -5, -5, -5, -5, -25, -20],
            [ 50, -20, -1, -1, -1, -1, -20,  50],
        ]

        self.assertEqual(table.table, init)

        table = Table(16)
        init = [
            [50, -20, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -20, 50],
            [-20, -25, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -25, -20],
            [-1, -5, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -5, -1],
            [-1, -5, -1, -25, -5, -5, -5, -5, -5, -5, -5, -5, -25, -1, -5, -1],
            [-1, -5, -1, -5, 0, -1, -1, -1, -1, -1, -1, 0, -5, -1, -5, -1],
            [-1, -5, -1, -5, -1, -25, -5, -5, -5, -5, -25, -1, -5, -1, -5, -1],
            [-1, -5, -1, -5, -1, -5, 0, -1, -1, 0, -5, -1, -5, -1, -5, -1],
            [-1, -5, -1, -5, -1, -5, -1, -1, -1, -1, -5, -1, -5, -1, -5, -1],
            [-1, -5, -1, -5, -1, -5, -1, -1, -1, -1, -5, -1, -5, -1, -5, -1],
            [-1, -5, -1, -5, -1, -5, 0, -1, -1, 0, -5, -1, -5, -1, -5, -1],
            [-1, -5, -1, -5, -1, -25, -5, -5, -5, -5, -25, -1, -5, -1, -5, -1],
            [-1, -5, -1, -5, 0, -1, -1, -1, -1, -1, -1, 0, -5, -1, -5, -1],
            [-1, -5, -1, -25, -5, -5, -5, -5, -5, -5, -5, -5, -25, -1, -5, -1],
            [-1, -5, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -5, -1],
            [-20, -25, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -25, -20],
            [50, -20, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -20, 50],
        ]

    def test_table_init_general(self):
        table = Table(4, corner=1, c=2, a1=3, a2=4, b1=5, b2=6, b3=7, x=8, o=9)
        init = [
            [3, 7, 7, 3],
            [7, 5, 5, 7],
            [7, 5, 5, 7],
            [3, 7, 7, 3],
        ]

        self.assertEqual(table.table, init)

        table = Table(6, corner=1, c=2, a1=3, a2=4, b1=5, b2=6, b3=7, x=8, o=9)
        init = [
            [1, 2, 4, 4, 2, 1],
            [2, 8, 7, 7, 8, 2],
            [4, 7, 5, 5, 7, 4],
            [4, 7, 5, 5, 7, 4],
            [2, 8, 7, 7, 8, 2],
            [1, 2, 4, 4, 2, 1],
        ]

        self.assertEqual(table.table, init)

    def test_table8_score(self):
        table = Table(8)
        board = Board(8)
        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 2)
        board.put_disc('black', 2, 3)
        board.put_disc('white', 4, 2)
        board.put_disc('black', 1, 1)
        board.put_disc('white', 0, 0)

        self.assertEqual(table.get_score('black', board), -22)
        self.assertEqual(table.get_score('white', board), 22)
        self.assertEqual(table.next_move('black', board), (5, 2))
        self.assertEqual(table.next_move('white', board), (2, 5))

        table.next_move('black', Board(4))
        init = [
            [0, -1, -1, 0],
            [-1, -1, -1, -1],
            [-1, -1, -1, -1],
            [0, -1, -1, 0],
        ]

        self.assertEqual(table.table, init)
