"""Tests of window.py
"""

import unittest
import tkinter as tk
import threading

import reversi
from reversi import Window


class TestWindow(unittest.TestCase):
    """window
    """
    def test_window_init(self):
        root = tk.Tk()
        b = ['Easy1', 'Normal1', 'Hard1']
        w = ['Easy2', 'Normal2', 'Hard2']
        window = Window(root=root, black_players=b, white_players=w)

        self.assertEqual(window.root, root)
        self.assertEqual(window.size, reversi.window.DEFAULT_BOARD_SIZE)
        self.assertEqual(window.player['black'], 'Easy1')
        self.assertEqual(window.player['white'], 'Easy2')
        self.assertEqual(window.assist, 'OFF')
        self.assertEqual(window.language, 'English')
        self.assertEqual(window.cancel, 'OK')
        self.assertEqual(window.cputime, reversi.window.CPU_TIME)
        self.assertEqual(window.extra_file, '')
        self.assertIsInstance(window.menu, reversi.window.Menu)
        self.assertIsInstance(window.canvas, tk.Canvas)

    def test_window_init_screen(self):
        root = tk.Tk()
        b = ['Easy1', 'Normal1', 'Hard1']
        w = ['Easy2', 'Normal2', 'Hard2']
        window = Window(root=root, black_players=b, white_players=w)
        window.init_screen()
        # canvas
        # width and height 設定値と不一致:要調査
        # board
        self.assertEqual(window.board.size, reversi.window.DEFAULT_BOARD_SIZE)
        self.assertEqual(window.board.cputime, reversi.window.CPU_TIME)
        self.assertEqual(window.board.assist, reversi.window.ASSIST_MENU[1])
        self.assertEqual(window.board._squares, [[None for _ in range(window.board.size)] for _ in range(window.board.size)])
        self.assertEqual(window.board._xlines, [6, 10, 14, 18, 22, 26, 30, 38, 40])
        self.assertEqual(window.board._ylines, [4, 8, 12, 16, 20, 24, 28, 36, 39])
        self.assertEqual(window.board.move, None)
        self.assertEqual(window.board.event.is_set(), False)
        # info
        self.assertEqual(window.info.player, {'black': b[0], 'white': w[0]})
        self.assertEqual(window.info.language, reversi.window.LANGUAGE_MENU[0])
        # start
        self.assertEqual(window.start.language, reversi.window.LANGUAGE_MENU[0])
        self.assertEqual(window.start.event.is_set(), False)

    def test_window_set_state(self):
        root = tk.Tk()
        b = ['Easy1', 'Normal1', 'Hard1']
        w = ['Easy2', 'Normal2', 'Hard2']
        window = Window(root=root, black_players=b, white_players=w)
        window.init_screen()

        class TestState:
            def __init__(self):
                self.state = None

            def set_state(self, state):
                self.state = state

        window.start = TestState()
        window.menu = TestState()

        window.set_state('Normal')
        self.assertEqual(window.start.state, 'Normal')
        self.assertEqual(window.menu.state, 'Normal')

        window.set_state('Disable')
        self.assertEqual(window.start.state, 'Disable')
        self.assertEqual(window.menu.state, 'Disable')

    def test_window_menu_init(self):
        root = tk.Tk()
        b = ['Easy1', 'Normal1', 'Hard1']
        w = ['Easy2', 'Normal2', 'Hard2']
        window = Window(root=root, black_players=b, white_players=w)
        self.assertIsInstance(window.menu.window, Window)
        self.assertEqual(window.menu.size, reversi.window.DEFAULT_BOARD_SIZE)
        self.assertEqual(window.menu.black_player, b[0])
        self.assertEqual(window.menu.white_player, w[0])
        self.assertEqual(window.menu.assist, reversi.window.ASSIST_MENU[1])
        self.assertEqual(window.menu.language, reversi.window.LANGUAGE_MENU[0])
        self.assertEqual(window.menu.cancel, reversi.window.CANCEL_MENU[0])
        self.assertIsInstance(window.menu.event, threading.Event)
        self.assertEqual(window.menu.menu_items['size'], range(reversi.board.MIN_BOARD_SIZE, reversi.board.MAX_BOARD_SIZE + 1, 2))
        self.assertEqual(window.menu.menu_items['black'], b)
        self.assertEqual(window.menu.menu_items['white'], w)
        self.assertEqual(window.menu.menu_items['cputime'], reversi.window.CPUTIME_MENU)
        self.assertEqual(window.menu.menu_items['extra'], reversi.window.EXTRA_MENU)
        self.assertEqual(window.menu.menu_items['assist'], reversi.window.ASSIST_MENU)
        self.assertEqual(window.menu.menu_items['language'], reversi.window.LANGUAGE_MENU)
        self.assertEqual(window.menu.menu_items['cancel'], reversi.window.CANCEL_MENU)
        for item in ['size', 'black', 'white', 'cputime', 'extra', 'assist', 'language', 'cancel']:
            self.assertIsInstance(window.menu.menus[item], tk.Menu)
