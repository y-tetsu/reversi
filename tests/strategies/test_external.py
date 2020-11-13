"""Tests of external.py
"""

import unittest
from test.support import captured_stdout
import os

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
        self.osname = os.name

        with open('./exit1.py', 'w') as wf:
            wf.write("import sys\n")
            wf.write("print('Error : exit(9)', file=sys.stderr)\n")
            wf.write("exit(9)\n")

    def tearDown(self):
        os.remove('./exit1.py')

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

    def test_external_next_move_cmd_illegal_finish_error(self):
        cmd = 'py -3.7 ./exit1.py' if self.osname == 'nt' else 'python ./exit1.py'
        external = External(cmd)
        external.error_message = error_message

        with captured_stdout() as stdout:
            external.next_move(self.color, self.board)

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], "プロセスが異常終了しました。終了ステータス(9)")
        self.assertEqual(lines[1], "(標準エラー出力)")
        self.assertEqual(lines[2], "Error : exit(9)")
