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

    def test_montecarlo_playout_large_size(self):
        montecarlo = MonteCarlo()
        montecarlo.remain = 4
        board = BitBoard(4)

        self.assertEqual(montecarlo._playout('black', board, (0, 1)), 0)

    def test_montecarlo_playout_draw(self):
        montecarlo = MonteCarlo()
        board = BitBoard(4)
        board.put_disc('black', 1, 0)
        board.put_disc('white', 0, 2)
        board.put_disc('black', 0, 3)
        board.put_disc('white', 0, 0)
        board.put_disc('black', 0, 1)
        board.put_disc('white', 2, 0)
        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 3)
        board.put_disc('black', 3, 0)
        board.put_disc('white', 1, 3)

        self.assertEqual(montecarlo._playout('black', board, (3, 3)), 0.5)

    def test_montecarlo_performance(self):
        board = BitBoard()
        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 4)
        board.put_disc('black', 1, 5)

        montecarlo = MonteCarlo(count=10000000)
        montecarlo.next_move('white', board)

        key = montecarlo.__class__.__name__ + str(os.getpid())
        print()
        print(key)
        print(' count(25000) :', Measure.count[key])
        print(' min          :', Measure.elp_time[key]['min'], '(s)')
        print(' max          :', Measure.elp_time[key]['max'], '(s)')
        print(' ave          :', Measure.elp_time[key]['ave'], '(s)')

    def test_montecarlo_force_import_error(self):
        import os
        import importlib
        import reversi

        # -------------------------------
        # switch environ and reload module
        os.environ['FORCE_MONTECARLOMETHODS_IMPORT_ERROR'] = 'RAISE'
        importlib.reload(reversi.strategies.MonteCarloMethods)
        self.assertTrue(reversi.strategies.MonteCarloMethods.SLOW_MODE)
        self.assertTrue(reversi.strategies.MonteCarloMethods.MONTECARLO_SIZE8_64BIT_ERROR)
        # -------------------------------

        board = BitBoard()
        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 4)
        board.put_disc('black', 1, 5)

        montecarlo = MonteCarlo(count=10000000)
        montecarlo.next_move('white', board)

        key = montecarlo.__class__.__name__ + str(os.getpid())
        print()
        print(key)
        print(' count(120)  :', Measure.count[key])
        print(' min         :', Measure.elp_time[key]['min'], '(s)')
        print(' max         :', Measure.elp_time[key]['max'], '(s)')
        print(' ave         :', Measure.elp_time[key]['ave'], '(s)')

        # -------------------------------
        # recover environment and reload module
        del os.environ['FORCE_MONTECARLOMETHODS_IMPORT_ERROR']
        importlib.reload(reversi.strategies.MonteCarloMethods)
        self.assertFalse(reversi.strategies.MonteCarloMethods.SLOW_MODE)
        self.assertFalse(reversi.strategies.MonteCarloMethods.MONTECARLO_SIZE8_64BIT_ERROR)
        # -------------------------------
