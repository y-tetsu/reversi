"""Tests of app.py
"""

import unittest
from test.support import captured_stdout

from reversi import Reversi, Reversic, Window
from reversi.strategies import WindowUserInput, ConsoleUserInput


class TestApp(unittest.TestCase):
    """app
    """
    def test_reversi_init(self):
        app = Reversi()

        self.assertEqual(app.state, app.INIT)
        self.assertIsInstance(app.window, Window)
        self.assertTrue('User1' in app.players_info)
        self.assertIsInstance(app.players_info['User1'], WindowUserInput)
        self.assertTrue('User2' in app.players_info)
        self.assertIsInstance(app.players_info['User2'], WindowUserInput)

    def test_reversi_state(self):
        app = Reversi()

        app.state = 'INIT'
        self.assertEqual(app.state, app.INIT)
        self.assertEqual(app.game, app._Reversi__init)

        app.state = 'DEMO'
        self.assertEqual(app.state, app.DEMO)
        self.assertEqual(app.game, app._Reversi__demo)

        app.state = 'PLAY'
        self.assertEqual(app.state, app.PLAY)
        self.assertEqual(app.game, app._Reversi__play)

        app.state = 'END'
        self.assertEqual(app.state, app.END)
        self.assertEqual(app.game, app._Reversi__end)

        app.state = 'REINIT'
        self.assertEqual(app.state, app.REINIT)
        self.assertEqual(app.game, app._Reversi__reinit)

        app.state = 'UNDEFINED'
        self.assertEqual(app.state, 'UNDEFINED')
        self.assertEqual(app.game, app._Reversi__reinit)

    def test_reversi_gameloop(self):
        app = Reversi()

        def test_game():
            print('test_game')
            return True

        app.game = test_game

        with captured_stdout() as stdout:
            app.gameloop()

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], 'test_game')

    def test_reversi_start(self):
        app = Reversi()

        def test_game_start():
            print('test_game_start')

        app.game_start = test_game_start

        def test_window_start():
            print('test_window_start')

        app.window_start = test_window_start

        with captured_stdout() as stdout:
            app.start()

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], 'test_game_start')
        self.assertEqual(lines[1], 'test_window_start')

    def test_reversi_game_start(self):
        app = Reversi()

        def test_thread_start(game_thread):
            print(game_thread.daemon)

        app._thread_start = test_thread_start

        with captured_stdout() as stdout:
            app.game_start()

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], 'True')

    def test_reversi_thread_start(self):
        app = Reversi()

        class TestThreadStart:
            def start(self):
                print('thread.start()')

        with captured_stdout() as stdout:
            app._thread_start(TestThreadStart())

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], 'thread.start()')

    def test_reversi_window_start(self):
        app = Reversi()

        class TestWindow:
            def __init__(self):
                class Root:
                    def deiconify(self):
                        print('deiconify')

                    def mainloop(self):
                        print('mainloop')

                self.root = Root()

        app.window = TestWindow()
        with captured_stdout() as stdout:
            app.window_start()

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], 'deiconify')
        self.assertEqual(lines[1], 'mainloop')

    def test_reversic_init(self):
        app = Reversic()

        self.assertEqual(app.board_size, 8)
        self.assertEqual(app.player_names, {'black': 'User1', 'white': 'User2'})
        self.assertEqual(app.state, app.START)
        self.assertTrue('User1' in app.players_info['black'])
        self.assertIsInstance(app.players_info['black']['User1'], ConsoleUserInput)
        self.assertTrue('User2' in app.players_info['white'])
        self.assertIsInstance(app.players_info['white']['User2'], ConsoleUserInput)
