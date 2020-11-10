"""Tests of external.py
"""

import unittest
from test.support import captured_stdout

import reversi
from reversi.strategies.external import External
from reversi.board import BitBoard


class TestExternal(unittest.TestCase):
    """external
    """
    def test_external_init(self):
        external = External()
        self.assertEqual(external.cmd, None)
        self.assertEqual(external.timeouttime, reversi.strategies.external.TIMEOUT_TIME)

    def test_external_next_move_no_cmd_error(self):
        def error_message(message):
            print(message)

        board = BitBoard()
        color = 'black'
        external = External()
        external.error_message = error_message

        with captured_stdout() as stdout:
            external.next_move(color, board)

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], "コマンドが設定されていません。")

    def test_external_next_move_cmd_timeout_error(self):
        import platform
        pf = platform.system()
        command = 'sleep 5'
        if pf == 'Windows':
            command = 'timeout 5'

        def error_message(message):
            print(message)

        board = BitBoard()
        color = 'black'
        external = External(command)
        external.timeouttime = 0.01
        external.error_message = error_message

        with captured_stdout() as stdout:
            external.next_move(color, board)

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], "コマンドがタイムアウトしました。")
