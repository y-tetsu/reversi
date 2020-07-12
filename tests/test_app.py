"""Tests of app.py
"""

import unittest

from reversi import Reversi, Reversic, Window
from reversi.strategies import WindowUserInput, ConsoleUserInput


class TestApp(unittest.TestCase):
    """app
    """
    def test_reversi_init(self):
        app = Reversi()

        self.assertEqual(app.state, app.INIT)
        self.assertIsInstance(app.window, Window)
        self.assertTrue('User1' in app.strategies)
        self.assertIsInstance(app.strategies['User1'], WindowUserInput)
        self.assertTrue('User2' in app.strategies)
        self.assertIsInstance(app.strategies['User2'], WindowUserInput)

    def test_reversic_init(self):
        app = Reversic()

        self.assertEqual(app.board_size, 8)
        self.assertEqual(app.player_names, {'black': 'User1', 'white': 'User2'})
        self.assertEqual(app.state, app.START)
        self.assertTrue('User1' in app.strategies['black'])
        self.assertIsInstance(app.strategies['black']['User1'], ConsoleUserInput)
        self.assertTrue('User2' in app.strategies['white'])
        self.assertIsInstance(app.strategies['white']['User2'], ConsoleUserInput)
