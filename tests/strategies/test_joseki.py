"""Tests of joseki.py
"""

import unittest
import os

from reversi.board import BitBoard
from reversi.strategies import AbstractStrategy, Random, _Joseki_, _Usagi_, Usagi
from reversi.strategies.common import Measure
from reversi.strategies.joseki import MOUSE, BULL, TIGER, SROSE, ROSEVILLE, FASTBOAT, CAT, RABBIT


class TestJoseki(unittest.TestCase):
    """joseki
    """
    def test_joseki_init(self):
        joseki = _Joseki_(Random())

        self.assertEqual(joseki.joseki, {})
        self.assertIsInstance(joseki.base, Random)

    def test_joseki_next_move(self):
        class Origin(AbstractStrategy):
            def next_move(self, color, board):
                return (0, 0)

        joseki = _Joseki_(Origin())
        board = BitBoard(4)
        self.assertEqual(joseki.next_move('black', board), (0, 0))

        board = BitBoard(8)
        self.assertEqual(joseki.next_move('black', board), (0, 0))

        joseki.joseki = {
            ('black', 0x0000000810000000, 0x0000001008000000): (5, 4),
        }
        self.assertEqual(joseki.next_move('black', board), (5, 4))

    def test_usagi_init(self):
        joseki = {}
        joseki.update(MOUSE)
        joseki.update(BULL)
        joseki.update(TIGER)
        joseki.update(SROSE)
        joseki.update(ROSEVILLE)
        joseki.update(FASTBOAT)
        joseki.update(CAT)
        joseki.update(RABBIT)

        # no Measure
        _usagi_ = _Usagi_(Random())
        key = _usagi_.__class__.__name__ + str(os.getpid())
        board = BitBoard()
        _usagi_.next_move('black', board)

        self.assertEqual(_usagi_.joseki, joseki)
        self.assertIsInstance(_usagi_.base, Random)
        self.assertFalse(key in Measure.elp_time)

        # with Measure
        usagi = Usagi(Random())
        key = usagi.__class__.__name__ + str(os.getpid())
        board = BitBoard()
        usagi.next_move('black', board)

        self.assertEqual(usagi.joseki, joseki)
        self.assertIsInstance(usagi.base, Random)
        self.assertTrue(key in Measure.elp_time)
