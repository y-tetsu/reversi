"""Tests of table.py
"""

import unittest

from reversi.board import Board
from reversi.strategies import Table


class TestTable(unittest.TestCase):
    """table
    """
    def test_table_init(self):
        table = Table(4)
        init = [
            [ 50, -20, -20,  50],  # noqa: E201
            [-20,  -1,  -1, -20],
            [-20,  -1,  -1, -20],
            [ 50, -20, -20,  50],  # noqa: E201
        ]

        self.assertEqual(table.table, init)

        table = Table(8)
        init = [
            [ 50, -20, -1, -1, -1, -1, -20,  50],  # noqa: E201
            [-20, -25, -5, -5, -5, -5, -25, -20],
            [ -1,  -5,  0, -1, -1,  0,  -5,  -1],  # noqa: E201
            [ -1,  -5, -1, -1, -1, -1,  -5,  -1],  # noqa: E201
            [ -1,  -5, -1, -1, -1, -1,  -5,  -1],  # noqa: E201
            [ -1,  -5,  0, -1, -1,  0,  -5,  -1],  # noqa: E201
            [-20, -25, -5, -5, -5, -5, -25, -20],
            [ 50, -20, -1, -1, -1, -1, -20,  50],  # noqa: E201
        ]

        self.assertEqual(table.table, init)

        table = Table(16)
        init = [
            [ 50, -20, -1,  -1, -1,  -1, -1, -1, -1, -1,  -1, -1,  -1, -1, -20,  50],  # noqa: E201
            [-20, -25, -5,  -5, -5,  -5, -5, -5, -5, -5,  -5, -5,  -5, -5, -25, -20],
            [ -1,  -5,  0,  -1, -1,  -1, -1, -1, -1, -1,  -1, -1,  -1,  0,  -5,  -1],  # noqa: E201
            [ -1,  -5, -1, -25, -5,  -5, -5, -5, -5, -5,  -5, -5, -25, -1,  -5,  -1],  # noqa: E201
            [ -1,  -5, -1,  -5,  0,  -1, -1, -1, -1, -1,  -1,  0,  -5, -1,  -5,  -1],  # noqa: E201
            [ -1,  -5, -1,  -5, -1, -25, -5, -5, -5, -5, -25, -1,  -5, -1,  -5,  -1],  # noqa: E201
            [ -1,  -5, -1,  -5, -1,  -5,  0, -1, -1,  0,  -5, -1,  -5, -1,  -5,  -1],  # noqa: E201
            [ -1,  -5, -1,  -5, -1,  -5, -1, -1, -1, -1,  -5, -1,  -5, -1,  -5,  -1],  # noqa: E201
            [ -1,  -5, -1,  -5, -1,  -5, -1, -1, -1, -1,  -5, -1,  -5, -1,  -5,  -1],  # noqa: E201
            [ -1,  -5, -1,  -5, -1,  -5,  0, -1, -1,  0,  -5, -1,  -5, -1,  -5,  -1],  # noqa: E201
            [ -1,  -5, -1,  -5, -1, -25, -5, -5, -5, -5, -25, -1,  -5, -1,  -5,  -1],  # noqa: E201
            [ -1,  -5, -1,  -5,  0,  -1, -1, -1, -1, -1,  -1,  0,  -5, -1,  -5,  -1],  # noqa: E201
            [ -1,  -5, -1, -25, -5,  -5, -5, -5, -5, -5,  -5, -5, -25, -1,  -5,  -1],  # noqa: E201
            [ -1,  -5,  0,  -1, -1,  -1, -1, -1, -1, -1,  -1, -1,  -1,  0,  -5,  -1],  # noqa: E201
            [-20, -25, -5,  -5, -5,  -5, -5, -5, -5, -5,  -5, -5,  -5, -5, -25, -20],
            [ 50, -20, -1,  -1, -1,  -1, -1, -1, -1, -1,  -1, -1,  -1, -1, -20,  50],  # noqa: E201
        ]

    def test_table_init_general(self):
        table = Table(4, corner=0, c=1, a1=2, a2=3, b1=4, b2=5, b3=6, x=7, o1=8, o2=9)
        init = [
            [0, 1, 1, 0],
            [1, 4, 4, 1],
            [1, 4, 4, 1],
            [0, 1, 1, 0],
        ]

        self.assertEqual(table.table, init)

        table = Table(6, corner=0, c=1, a1=2, a2=3, b1=4, b2=5, b3=6, x=7, o1=8, o2=9)
        init = [
            [0, 1, 3, 3, 1, 0],
            [1, 7, 8, 8, 7, 1],
            [3, 8, 4, 4, 8, 3],
            [3, 8, 4, 4, 8, 3],
            [1, 7, 8, 8, 7, 1],
            [0, 1, 3, 3, 1, 0],
        ]

        self.assertEqual(table.table, init)

        table = Table(8, corner=0, c=1, a1=2, a2=3, b1=4, b2=5, b3=6, x=7, o1=8, o2=9)
        init = [
            [0, 1, 3, 6, 6, 3, 1, 0],
            [1, 7, 8, 9, 9, 8, 7, 1],
            [3, 8, 2, 5, 5, 2, 8, 3],
            [6, 9, 5, 4, 4, 5, 9, 6],
            [6, 9, 5, 4, 4, 5, 9, 6],
            [3, 8, 2, 5, 5, 2, 8, 3],
            [1, 7, 8, 9, 9, 8, 7, 1],
            [0, 1, 3, 6, 6, 3, 1, 0],
        ]

        self.assertEqual(table.table, init)

        table = Table(16, corner=0, c=1, a1=2, a2=3, b1=4, b2=5, b3=6, x=7, o1=8, o2=9)
        init = [
            [0, 1, 3, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 3, 1, 0],
            [1, 7, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 8, 7, 1],
            [3, 8, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 8, 3],
            [6, 9, 5, 7, 8, 9, 9, 9, 9, 9, 9, 8, 7, 5, 9, 6],
            [6, 9, 5, 8, 2, 5, 5, 5, 5, 5, 5, 2, 8, 5, 9, 6],
            [6, 9, 5, 9, 5, 7, 8, 9, 9, 8, 7, 5, 9, 5, 9, 6],
            [6, 9, 5, 9, 5, 8, 2, 5, 5, 2, 8, 5, 9, 5, 9, 6],
            [6, 9, 5, 9, 5, 9, 5, 4, 4, 5, 9, 5, 9, 5, 9, 6],
            [6, 9, 5, 9, 5, 9, 5, 4, 4, 5, 9, 5, 9, 5, 9, 6],
            [6, 9, 5, 9, 5, 8, 2, 5, 5, 2, 8, 5, 9, 5, 9, 6],
            [6, 9, 5, 9, 5, 7, 8, 9, 9, 8, 7, 5, 9, 5, 9, 6],
            [6, 9, 5, 8, 2, 5, 5, 5, 5, 5, 5, 2, 8, 5, 9, 6],
            [6, 9, 5, 7, 8, 9, 9, 9, 9, 9, 9, 8, 7, 5, 9, 6],
            [3, 8, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 8, 3],
            [1, 7, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 8, 7, 1],
            [0, 1, 3, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 3, 1, 0],
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

        self.assertEqual(table.get_score(board), -22)
        self.assertEqual(table.next_move('black', board), (5, 2))
        self.assertEqual(table.next_move('white', board), (2, 5))

        table.next_move('black', Board(4))
        init = [
            [ 50, -20, -20,  50],  # noqa: E201
            [-20,  -1,  -1, -20],
            [-20,  -1,  -1, -20],
            [ 50, -20, -20,  50],  # noqa: E201
        ]

        self.assertEqual(table.table, init)

    def test_table_force_import_error(self):
        import os
        import importlib
        import reversi

        # -------------------------------
        # switch environ and reload module
        os.environ['FORCE_TABLEMETHODS_IMPORT_ERROR'] = 'RAISE'
        importlib.reload(reversi.strategies.TableMethods)
        self.assertTrue(reversi.strategies.TableMethods.SLOW_MODE)
        # -------------------------------

        # size8
        table = Table(8)
        board = Board(8)
        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 2)
        board.put_disc('black', 2, 3)
        board.put_disc('white', 4, 2)
        board.put_disc('black', 1, 1)
        board.put_disc('white', 0, 0)
        self.assertEqual(table.get_score(board), -22)

        # -------------------------------
        # recover environment and reload module
        del os.environ['FORCE_TABLEMETHODS_IMPORT_ERROR']
        importlib.reload(reversi.strategies.TableMethods)
        self.assertFalse(reversi.strategies.TableMethods.SLOW_MODE)
        # -------------------------------
