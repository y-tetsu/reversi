"""Tests of disc.py
"""

import unittest

from reversi.disc import Black, White, Blank, DiscFactory, D


class TestDisc(unittest.TestCase):
    """disc
    """
    def test_disc_black_class(self):
        f = DiscFactory()
        black = f.create('black')
        self.assertIsInstance(black, Black)

    def test_disc_black_mark(self):
        f = DiscFactory()
        black = f.create('black')
        self.assertEqual(black, '〇')

    def test_disc_white_class(self):
        f = DiscFactory()
        white = f.create('white')
        self.assertIsInstance(white, White)

    def test_disc_white_mark(self):
        f = DiscFactory()
        white = f.create('white')
        self.assertEqual(white, '●')

    def test_disc_blank_class(self):
        f = DiscFactory()
        blank = f.create('blank')
        self.assertIsInstance(blank, Blank)

    def test_disc_blank_mark(self):
        f = DiscFactory()
        blank = f.create('blank')
        self.assertEqual(blank, '□')

    def test_disc_discs(self):
        self.assertEqual(D['black'], '〇')
        self.assertEqual(D['white'], '●')
        self.assertEqual(D['blank'], '□')
