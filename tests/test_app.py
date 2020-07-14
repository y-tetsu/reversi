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
        self.assertTrue('User1' in app.players_list)
        self.assertIsInstance(app.players_list['User1'], WindowUserInput)
        self.assertTrue('User2' in app.players_list)
        self.assertIsInstance(app.players_list['User2'], WindowUserInput)

    def test_reversic_init(self):
        app = Reversic()

        self.assertEqual(app.board_size, 8)
        self.assertEqual(app.player_names, {'black': 'User1', 'white': 'User2'})
        self.assertEqual(app.state, app.START)
        self.assertTrue('User1' in app.players_list['black'])
        self.assertIsInstance(app.players_list['black']['User1'], ConsoleUserInput)
        self.assertTrue('User2' in app.players_list['white'])
        self.assertIsInstance(app.players_list['white']['User2'], ConsoleUserInput)
