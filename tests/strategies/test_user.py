"""Tests of user.py
"""

import unittest
from test.support import captured_stdin, captured_stdout
import re

from reversi.board import Board
from reversi.strategies import ConsoleUserInput, WindowUserInput


class TestUser(unittest.TestCase):
    """user
    """
    def test_consoleuserinput_init(self):
        console_user_input = ConsoleUserInput()
        self.assertEqual(console_user_input.digit, re.compile('^[0-9]+$'))

    def test_consoleuserinput_is_digit(self):
        console_user_input = ConsoleUserInput()
        self.assertTrue(console_user_input._is_digit('000'))
        self.assertTrue(console_user_input._is_digit('123'))
        self.assertTrue(console_user_input._is_digit('999'))
        self.assertFalse(console_user_input._is_digit('０１２'))
        self.assertFalse(console_user_input._is_digit('abc'))
        self.assertFalse(console_user_input._is_digit('12z'))

    def test_consoleuserinput_next_move(self):
        board = Board()
        console_user_input = ConsoleUserInput()

        move = None
        with captured_stdin() as stdin:
            stdin.write('1')
            stdin.seek(0)
            move = console_user_input.next_move('black', board)

        self.assertEqual(move, (3, 2))

        move = None
        with captured_stdin() as stdin:
            stdin.write('2')
            stdin.seek(0)
            move = console_user_input.next_move('black', board)

        self.assertEqual(move, (2, 3))

    def test_windowuserinput_init(self):
        window_user_input = WindowUserInput(None)
        self.assertEqual(window_user_input.window, None)

    def test_windowuserinput_next_move(self):
        class TestWindow:
            def __init__(self):
                class Board:
                    def __init__(self):
                        class Event:
                            def __init__(self):
                                self.is_set = lambda: True

                            def clear(self):
                                print('clear')

                        self.move = (3, 2)
                        self.event = Event()

                    def selectable_moves(self, moves):
                        print('selectable_moves', moves)

                    def unselectable_moves(self, moves):
                        print('unselectable_moves', moves)

                self.board = Board()

                class Menu:
                    def __init__(self):
                        class Event:
                            def __init__(self):
                                self.count = 0

                            def is_set(self):
                                self.count += 1
                                print('is_set', self.count)
                                if self.count >= 2:
                                    return True
                                return False

                        self.event = Event()

                self.menu = Menu()

        # window.board.event.is_set True
        with captured_stdout() as stdout:
            window_user_input = WindowUserInput(TestWindow())
            move = window_user_input.next_move('black', Board())

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], 'selectable_moves [(3, 2), (2, 3), (5, 4), (4, 5)]')
        self.assertEqual(lines[1], 'is_set 1')
        self.assertEqual(lines[2], 'clear')
        self.assertEqual(lines[3], 'unselectable_moves [(3, 2), (2, 3), (5, 4), (4, 5)]')

        with self.assertRaises(IndexError):
            print(lines[4])

        self.assertEqual(move, (3, 2))

        # window.board.event.is_set False, and window.menu.event.is_set True(at second time)
        with captured_stdout() as stdout:
            window_user_input = WindowUserInput(TestWindow())
            window_user_input.window.board.event.is_set = lambda: False
            move = window_user_input.next_move('black', Board())

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], 'selectable_moves [(3, 2), (2, 3), (5, 4), (4, 5)]')
        self.assertEqual(lines[1], 'is_set 1')
        self.assertEqual(lines[2], 'is_set 2')

        with self.assertRaises(IndexError):
            print(lines[3])

        self.assertEqual(move, (3, 3))
