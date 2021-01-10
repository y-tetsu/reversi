"""Tests of player.py
"""

import unittest

from reversi.board import Board, BitBoard
from reversi.disc import D
from reversi.player import Player


class TestPlayer(unittest.TestCase):
    """player
    """
    def test_player(self):
        class TestStrategy:
            def __init__(self):
                self.cnt = 0

            def next_move(self, color, board):
                if self.cnt == 0:
                    self.cnt += 1
                    return (5, 4)

                return (3, 2)

        # ----- #
        # Board #
        # ----- #
        board = Board(8)
        p = Player('black', 'TestPlayer', TestStrategy())

        # init
        self.assertEqual(p.color, 'black')
        self.assertEqual(p.disc, D[p.color])
        self.assertEqual(p.name, 'TestPlayer')
        self.assertIsInstance(p.strategy, TestStrategy)
        self.assertEqual(p.move, (None, None))
        self.assertEqual(p.captures, [])

        # str
        self.assertEqual(str(p), D[p.color] + 'TestPlayer')

        # put_disc
        p.put_disc(board)
        self.assertEqual(p.move, (5, 4))
        self.assertEqual(p.captures, [(4, 4)])

        p.put_disc(board)
        self.assertEqual(p.move, (3, 2))
        self.assertEqual(p.captures, [(3, 3)])

        # -------- #
        # BitBoard #
        # -------- #
        board = BitBoard(8)
        p = Player('black', 'TestPlayer', TestStrategy())

        # init
        self.assertEqual(p.color, 'black')
        self.assertEqual(p.disc, D[p.color])
        self.assertEqual(p.name, 'TestPlayer')
        self.assertIsInstance(p.strategy, TestStrategy)
        self.assertEqual(p.move, (None, None))
        self.assertEqual(p.captures, [])

        # str
        self.assertEqual(str(p), D[p.color] + 'TestPlayer')

        # put_disc
        p.put_disc(board)
        self.assertEqual(p.move, (5, 4))
        self.assertEqual(p.captures, [(4, 4)])

        p.put_disc(board)
        self.assertEqual(p.move, (3, 2))
        self.assertEqual(p.captures, [(3, 3)])
