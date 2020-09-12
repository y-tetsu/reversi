"""Tests of window.py
"""

import unittest
import tkinter as tk

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
        self.assertEqual(window.canvas.winfo_reqwidth(), reversi.window.WINDOW_WIDTH+4)    # 設定値と不一致:要調査
        self.assertEqual(window.canvas.winfo_reqheight(), reversi.window.WINDOW_HEIGHT+4)  # 設定値と不一致:要調査
        # board
        self.assertEqual(window.board.canvas.winfo_reqwidth(), reversi.window.WINDOW_WIDTH+4)
        self.assertEqual(window.board.canvas.winfo_reqheight(), reversi.window.WINDOW_HEIGHT+4)
        self.assertEqual(window.board.size, reversi.window.DEFAULT_BOARD_SIZE)
        self.assertEqual(window.board.cputime, reversi.window.CPU_TIME)
        self.assertEqual(window.board.assist, reversi.window.ASSIST_MENU[1])
        self.assertEqual(window.board._squares, [[None for _ in range(window.board.size)] for _ in range(window.board.size)])
        self.assertEqual(window.board._xlines, [6, 10, 14, 18, 22, 26, 30, 38, 40])
        self.assertEqual(window.board._ylines, [4, 8, 12, 16, 20, 24, 28, 36, 39])
        self.assertEqual(window.board.move, None)
        self.assertEqual(window.board.event.is_set(), False)
        # info
        self.assertEqual(window.info.canvas.winfo_reqwidth(), reversi.window.WINDOW_WIDTH+4)
        self.assertEqual(window.info.canvas.winfo_reqheight(), reversi.window.WINDOW_HEIGHT+4)
        self.assertEqual(window.info.player, {'black': b[0], 'white': w[0]})
        self.assertEqual(window.info.language, reversi.window.LANGUAGE_MENU[0])
        # start
        self.assertEqual(window.start.canvas.winfo_reqwidth(), reversi.window.WINDOW_WIDTH+4)
        self.assertEqual(window.start.canvas.winfo_reqheight(), reversi.window.WINDOW_HEIGHT+4)
        self.assertEqual(window.start.language, reversi.window.LANGUAGE_MENU[0])
        self.assertEqual(window.start.event.is_set(), False)
