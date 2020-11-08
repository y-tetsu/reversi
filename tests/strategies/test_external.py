"""Tests of external.py
"""

import unittest

import reversi
from reversi.strategies.external import External


class TestExternal(unittest.TestCase):
    """external
    """
    def test_external_init(self):
        external = External()
        self.assertEqual(external.cmd, None)
        self.assertEqual(external.timeouttime, reversi.strategies.external.TIMEOUT_TIME)
