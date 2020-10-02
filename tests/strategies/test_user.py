"""Tests of user.py
"""

import unittest
from test.support import captured_stdin
import re

from reversi.board import Board
from reversi.strategies import ConsoleUserInput


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
