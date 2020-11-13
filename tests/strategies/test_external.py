"""Tests of external.py
"""

import unittest
from test.support import captured_stdout

import reversi
from reversi.strategies.external import External
from reversi.board import BitBoard


def error_message(message):
    print(message)


class TestExternal(unittest.TestCase):
    """external
    """
    def setUp(self):
        self.board = BitBoard()
        self.color = 'black'

    def test_external_init(self):
        external = External()
        self.assertEqual(external.cmd, None)
        self.assertEqual(external.timeouttime, reversi.strategies.external.TIMEOUT_TIME)

    def test_external_next_move_no_cmd_error(self):
        external = External()
        external.error_message = error_message

        with captured_stdout() as stdout:
            external.next_move(self.color, self.board)

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], "コマンドが設定されていません。")

    def test_external_next_move_cmd_timeout_error(self):
        external = External('more')
        external.timeouttime = 0
        external.error_message = error_message

        with captured_stdout() as stdout:
            external.next_move(self.color, self.board)

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], "コマンドがタイムアウトしました。")
