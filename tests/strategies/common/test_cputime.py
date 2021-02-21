"""Tests of cputime.py
"""

import unittest

from reversi.strategies.common import CPU_TIME


class TestCputime(unittest.TestCase):
    """cputime
    """
    def test_cputime(self):
        self.assertEqual(CPU_TIME, 0.5)
