"""Tests of disc.py
"""

import unittest

from reversi.color import C as c
from reversi.disc import Disc, Black, White, Blank, DiscFactory, D


class TestDisc(unittest.TestCase):
    """disc
    """
    def test_disc_black_class(self):
        black = DiscFactory().create(c.black)
        self.assertIsInstance(black, Black)
        self.assertEqual(black, '〇')

    def test_disc_white(self):
        white = DiscFactory().create(c.white)
        self.assertIsInstance(white, White)
        self.assertEqual(white, '●')

    def test_disc_blank(self):
        blank = DiscFactory().create(c.blank)
        self.assertIsInstance(blank, Blank)
        self.assertEqual(blank, '□')

    def test_disc_unknown(self):
        unknown = DiscFactory().create('unknown')
        self.assertIsInstance(unknown, Disc)
        self.assertEqual(unknown, '')

    def test_disc_d(self):
        self.assertEqual(D[c.black], '〇')
        self.assertEqual(D[c.white], '●')
        self.assertEqual(D[c.blank], '□')
