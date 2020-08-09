"""Tests of timer.py
"""

import unittest
import os
import time

from reversi.strategies.common import Timer, CPU_TIME


class TestTimer(unittest.TestCase):
    """timer
    """
    def test_time_limit(self):
        self.assertEqual(Timer.time_limit, CPU_TIME)

    def test_get_pid(self):
        pid1 = self.__class__.__name__ + str(os.getpid())
        pid2 = Timer.get_pid(self)
        self.assertEqual(pid1, pid2)

    def test_deadline(self):
        pid = Timer.get_pid(self)
        deadline = time.time() + Timer.time_limit
        Timer.set_deadline(pid, -10000)
        self.assertGreaterEqual(Timer.deadline[pid], deadline)
        self.assertFalse(Timer.timeout_flag[pid])
        self.assertEqual(Timer.timeout_value[pid], -10000)

    def test_start(self):
        value = -100

        class Dummy:
            def __init__(self):
                self.dummy = False

            @Timer.start(value)
            def timer_start(self):
                self.dummy = True

        deadline = time.time() + Timer.time_limit
        dummy = Dummy()
        dummy.timer_start()
        pid = dummy.__class__.__name__ + str(os.getpid())
        self.assertTrue(dummy.dummy)
        self.assertGreaterEqual(Timer.deadline[pid], deadline)
        self.assertFalse(Timer.timeout_flag[pid])
        self.assertEqual(Timer.timeout_value[pid], value)

    def test_timeout(self):
        pre_limit = Timer.time_limit
        value = -100

        class Dummy:
            def __init__(self):
                self.dummy = False

            @Timer.start(value)
            def timer_start(self):
                self.dummy = True

            @Timer.timeout
            def timeout_monitor(self, pid=None):
                self.dummy2 = True

        dummy = Dummy()
        dummy.timer_start()
        pid = dummy.__class__.__name__ + str(os.getpid())
        self.assertFalse(Timer.timeout_flag[pid])

        dummy.timeout_monitor(pid=pid)
        self.assertFalse(Timer.timeout_flag[pid])

        time.sleep(Timer.time_limit * 1.1)
        dummy.timeout_monitor(pid=pid)
        self.assertTrue(Timer.timeout_flag[pid])

        Timer.time_limit = pre_limit

    def test_is_timeout(self):
        pre_limit = Timer.time_limit
        value = -100

        class Dummy:
            def __init__(self):
                self.dummy = False

            @Timer.start(value)
            def timer_start(self):
                self.dummy = True

            @Timer.timeout
            def timeout_monitor(self, pid=None):
                self.dummy2 = True

        dummy = Dummy()
        dummy.timer_start()
        pid = dummy.__class__.__name__ + str(os.getpid())
        dummy.timeout_monitor(pid=pid)

        self.assertFalse(Timer.is_timeout(pid))

        time.sleep(Timer.time_limit * 1.1)
        dummy.timeout_monitor(pid=pid)

        self.assertTrue(Timer.is_timeout(pid))

        Timer.time_limit = pre_limit

    def test_multi(self):
        pre_limit = Timer.time_limit
        value = -100

        class Dummy1:
            def __init__(self):
                self.dummy = False

            @Timer.start(value)
            def timer_start(self):
                self.dummy = True

            @Timer.timeout
            def timeout_monitor(self, pid=None):
                self.dummy2 = True

        class Dummy2:
            def __init__(self):
                self.dummy = False

            @Timer.start(value)
            def timer_start(self):
                self.dummy = True

            @Timer.timeout
            def timeout_monitor(self, pid=None):
                self.dummy2 = True

        dummy1 = Dummy1()
        dummy2 = Dummy2()
        pid1 = dummy1.__class__.__name__ + str(os.getpid())
        pid2 = dummy2.__class__.__name__ + str(os.getpid())
        self.assertFalse(Timer.is_timeout(pid1))
        self.assertFalse(Timer.is_timeout(pid2))

        # (1st)
        # dummy1 start
        dummy1.timer_start()

        # time elapsed
        time.sleep((Timer.time_limit/2)*1.1)
        dummy1.timeout_monitor(pid=pid1)
        self.assertFalse(Timer.is_timeout(pid1))
        self.assertFalse(Timer.is_timeout(pid2))

        # dummy2 start
        dummy2.timer_start()

        # time elapsed and dummy1 timeout
        time.sleep((Timer.time_limit/2)*1.1)
        dummy1.timeout_monitor(pid=pid1)
        dummy2.timeout_monitor(pid=pid2)
        self.assertTrue(Timer.is_timeout(pid1))
        self.assertFalse(Timer.is_timeout(pid2))

        # time elapsed and dummy2 timeout
        time.sleep((Timer.time_limit/2)*1.1)
        dummy1.timeout_monitor(pid=pid1)
        dummy2.timeout_monitor(pid=pid2)
        self.assertTrue(Timer.is_timeout(pid1))
        self.assertTrue(Timer.is_timeout(pid2))

        # (2nd)
        # dummy1 start
        dummy1.timer_start()

        # time elapsed
        time.sleep((Timer.time_limit/2)*1.1)
        dummy1.timeout_monitor(pid=pid1)
        self.assertFalse(Timer.is_timeout(pid1))
        self.assertTrue(Timer.is_timeout(pid2))

        # dummy2 start
        dummy2.timer_start()

        # time elapsed and dummy1 timeout
        time.sleep((Timer.time_limit/2)*1.1)
        dummy1.timeout_monitor(pid=pid1)
        dummy2.timeout_monitor(pid=pid2)
        self.assertTrue(Timer.is_timeout(pid1))
        self.assertFalse(Timer.is_timeout(pid2))

        # time elapsed and dummy2 timeout
        time.sleep((Timer.time_limit/2)*1.1)
        dummy1.timeout_monitor(pid=pid1)
        dummy2.timeout_monitor(pid=pid2)
        self.assertTrue(Timer.is_timeout(pid1))
        self.assertTrue(Timer.is_timeout(pid2))

        Timer.time_limit = pre_limit
