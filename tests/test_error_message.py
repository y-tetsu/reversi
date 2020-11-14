"""Tests of error_message.py
"""

import unittest
from test.support import captured_stdout

from reversi import ErrorMessage


class TestErrorMessage(unittest.TestCase):
    """error_message
    """
    def test_error_message_init(self):
        err_msg = ErrorMessage()
        self.assertIsNone(err_msg.root)
        self.assertIsNone(err_msg.label)
        self.assertEqual(err_msg.title, 'Error')
        self.assertEqual(err_msg.minx, 300)
        self.assertEqual(err_msg.miny, 30)
        self.assertEqual(err_msg.fill, 'x')
        self.assertEqual(err_msg.padx, '5')
        self.assertEqual(err_msg.pady, '5')

    def test_error_message_show(self):
        err_msg = ErrorMessage()
        err_msg._start_window = lambda: print('start_window')
        with captured_stdout() as stdout:
            err_msg.show('test_show')

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], 'start_window')
        self.assertEqual(err_msg.label.cget('text'), 'test_show')

    def test_error_message_start_window(self):
        class TestRoot:
            def mainloop(self):
                print('mainloop')

        err_msg = ErrorMessage()
        err_msg.root = TestRoot()
        with captured_stdout() as stdout:
            err_msg._start_window()

        lines = stdout.getvalue().splitlines()
        self.assertEqual(lines[0], 'mainloop')
