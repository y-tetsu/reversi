"""Tests of timer.py
"""

import unittest
import os
import time

from reversi.strategies.common import Timer, CPU_TIME


class TestTimer(unittest.TestCase):
    """timer
    """
    def test_get_pid(self):
        pid1 = self.__class__.__name__ + str(os.getpid())
        pid2 = Timer.get_pid(self)
        self.assertEqual(pid1, pid2)

    def test_dedline(self):
        pid = Timer.get_pid(self)
        Timer.set_deadline(pid, -10000)
        self.assertEqual(Timer.deadline[pid], time.time() + CPU_TIME)
        self.assertFalse(Timer.timeout_flag[pid])
        self.assertEqual(Timer.timeout_value[pid], -10000)

    def test_start(self):
        pre_limit = Timer.time_limit
        limit, value = 100, -100

        class Dummy:
            def __init__(self):
                self.dummy = False

            @Timer.start(limit, value)
            def test_method(self):
                self.dummy = True

        dummy = Dummy()
        self.assertEqual(Timer.time_limit, limit)
        dummy.test_method()
        pid = dummy.__class__.__name__ + str(os.getpid())
        self.assertTrue(dummy.dummy)
        self.assertGreaterEqual(Timer.deadline[pid], time.time() + limit)
        self.assertFalse(Timer.timeout_flag[pid])
        self.assertEqual(Timer.timeout_value[pid], value)
        Timer.time_limit = pre_limit
