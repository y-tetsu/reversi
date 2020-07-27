"""Tests of player.py
"""

import unittest

from reversi.board import Board, BitBoard
from reversi.player import Player


class TestPlayer(unittest.TestCase):
    """player
    """
    def test_player(self):
        class TestStrategy:
            def next_move(self, color, board):
                return (5, 4)

        # ----- #
        # Board #
        # ----- #
        board = Board(8)
        p = Player('black', 'TestPlayer', TestStrategy())

        # init
        self.assertEqual(p.color, 'black')
        self.assertEqual(p.disc, board.disc[p.color])
        self.assertEqual(p.name, 'TestPlayer')
        self.assertIsInstance(p.strategy, TestStrategy)
        self.assertEqual(p.move, (None, None))
        self.assertEqual(p.captures, [])

        # str
        self.assertEqual(str(p), board.disc[p.color] + 'TestPlayer')

        # put_disc
        p.put_disc(board)
        self.assertEqual(p.move, (5, 4))
        self.assertEqual(p.captures, [(4, 4)])

        # -------- #
        # BitBoard #
        # -------- #
        board = BitBoard(8)
        p = Player('black', 'TestPlayer', TestStrategy())

        # init
        self.assertEqual(p.color, 'black')
        self.assertEqual(p.disc, board.disc[p.color])
        self.assertEqual(p.name, 'TestPlayer')
        self.assertIsInstance(p.strategy, TestStrategy)
        self.assertEqual(p.move, (None, None))
        self.assertEqual(p.captures, [])

        # str
        self.assertEqual(str(p), board.disc[p.color] + 'TestPlayer')

        # put_disc
        p.put_disc(board)
        self.assertEqual(p.move, (5, 4))
        self.assertEqual(p.captures, [(4, 4)])
