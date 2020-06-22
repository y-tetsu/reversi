"""Tests of table.py
"""

import unittest

import numpy as np

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

        self.assertTrue((table.table == np.array(init)).all())

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

        self.assertTrue((table.table == np.array(init)).all())

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

        self.assertTrue((table.table == np.array(init)).all())

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

        self.assertTrue((table.table == np.array(init)).all())
