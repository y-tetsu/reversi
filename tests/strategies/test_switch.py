"""Tests of switch.py
"""

import unittest

from reversi.board import Board
from reversi.strategies.switch import Switch, SwitchSizeError
from reversi.strategies import Random, Unselfish, Greedy
from reversi.strategies.common import AbstractStrategy


class TestSwitch(unittest.TestCase):
    """switch
    """
    def test_switch_size_error(self):
        with self.assertRaises(SwitchSizeError):
            Switch(turns=[0, 1], strategies=[0])

    def test_switch_init(self):
        turns = [10, 20, 30, 40, 50, 60]
        strategies = [Random(), Unselfish(), Greedy(), Random(), Unselfish(), Greedy()]
        switch = Switch(
            turns=turns,
            strategies=strategies,
        )

        self.assertEqual(switch.turns, turns)
        self.assertEqual(switch.strategies, strategies)

    def test_switch_next_move(self):
        class Put_5_4(AbstractStrategy):
            def next_move(self, color, board):
                return (5, 4)

        class Put_5_5(AbstractStrategy):
            def next_move(self, color, board):
                return (5, 5)

        class Put_4_5(AbstractStrategy):
            def next_move(self, color, board):
                return (4, 5)

        switch = Switch(
            turns=[0, 1, 2],
            strategies=[Put_5_4(), Put_5_5(), Put_4_5()],
        )

        board = Board()
        move = switch.next_move('black', board)
        self.assertEqual(move, (5, 4))
        board.put_disc('black', *move)

        move = switch.next_move('white', board)
        self.assertEqual(move, (5, 5))
        board.put_disc('white', *move)

        move = switch.next_move('black', board)
        self.assertEqual(move, (4, 5))
        board.put_disc('black', *move)
