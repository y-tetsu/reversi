"""Tests of disc.py
"""

import unittest
from reversi.disc import Black, White, Blank, DiscFactory


class TestDisc(unittest.TestCase):
    """disc
    """
    def test_disc_black_class(self):
        f = DiscFactory()
        black = f.create('black')
        assert isinstance(black, Black)

    def test_disc_black_mark(self):
        f = DiscFactory()
        black = f.create('black')
        assert black == '〇'

    def test_disc_white_class(self):
        f = DiscFactory()
        white = f.create('white')
        assert isinstance(white, White)

    def test_disc_white_mark(self):
        f = DiscFactory()
        white = f.create('white')
        assert white == '●'

    def test_disc_blank_class(self):
        f = DiscFactory()
        blank = f.create('blank')
        assert isinstance(blank, Blank)

    def test_disc_blank_mark(self):
        f = DiscFactory()
        blank = f.create('blank')
        assert blank == '□'
