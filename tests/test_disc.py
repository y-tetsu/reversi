"""Tests of disc.py
"""

import unittest

from reversi.color import C as c
from reversi.disc import Disc, Black, White, Blank, DiscFactory, DiscDictAttributeError, D


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

    def test_disc_dict(self):
        self.assertEqual(D[c.black], '〇')
        self.assertEqual(D[c.white], '●')
        self.assertEqual(D[c.blank], '□')
        self.assertEqual(D.black, '〇')
        self.assertEqual(D.white, '●')
        self.assertEqual(D.blank, '□')

    def test_disc_dict_is_black(self):
        self.assertTrue(D.is_black('〇'))
        self.assertFalse(D.is_black('●'))
        self.assertFalse(D.is_black('□'))
        self.assertFalse(D.is_black('＊'))

    def test_disc_dict_is_white(self):
        self.assertFalse(D.is_white('〇'))
        self.assertTrue(D.is_white('●'))
        self.assertFalse(D.is_white('□'))
        self.assertFalse(D.is_white('＊'))

    def test_disc_dict_is_blank(self):
        self.assertFalse(D.is_blank('〇'))
        self.assertFalse(D.is_blank('●'))
        self.assertTrue(D.is_blank('□'))
        self.assertFalse(D.is_blank('＊'))

    def test_disc_dict_property(self):
        with self.assertRaises(AttributeError):
            D.black = 'another disc'
        with self.assertRaises(AttributeError):
            D.white = 'another disc'
        with self.assertRaises(AttributeError):
            D.blank = 'another disc'
        with self.assertRaises(DiscDictAttributeError):
            D[c.black] = 'another disc'
        with self.assertRaises(DiscDictAttributeError):
            D[c.white] = 'another disc'
        with self.assertRaises(DiscDictAttributeError):
            D[c.blank] = 'another disc'
        with self.assertRaises(DiscDictAttributeError):
            del D[c.black]
        with self.assertRaises(DiscDictAttributeError):
            del D[c.white]
        with self.assertRaises(DiscDictAttributeError):
            del D[c.blank]
