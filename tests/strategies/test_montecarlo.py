"""Tests of montecarlo.py
"""

import unittest
import os

from reversi.board import BitBoard
from reversi.strategies.common import Measure
from reversi.strategies import Random, MonteCarlo


class TestMonteCarlo(unittest.TestCase):
    """montecarlo
    """
    def test_montecarlo_init(self):
        montecarlo = MonteCarlo()

        self.assertEqual(montecarlo.count, 100)
        self.assertEqual(montecarlo.remain, 60)
        self.assertEqual(montecarlo._black_player.color, 'black')
        self.assertEqual(montecarlo._black_player.name, 'Random_B')
        self.assertIsInstance(montecarlo._black_player.strategy, Random)
        self.assertEqual(montecarlo._white_player.color, 'white')
        self.assertEqual(montecarlo._white_player.name, 'Random_W')
        self.assertIsInstance(montecarlo._white_player.strategy, Random)

    def test_montecarlo_performance(self):
        board = BitBoard()
        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 4)
        board.put_disc('black', 1, 5)

        montecarlo = MonteCarlo()
        montecarlo.next_move('white', board)

        key = montecarlo.__class__.__name__ + str(os.getpid())
        print()
        print(key)
        print(' count(120) :', Measure.count[key])
        print(' min        :', Measure.elp_time[key]['min'], '(s)')
        print(' max        :', Measure.elp_time[key]['max'], '(s)')
        print(' ave        :', Measure.elp_time[key]['ave'], '(s)')
