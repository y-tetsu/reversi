"""Tests of color.py
"""

import unittest

from reversi.color import Color, C


class TestColor(unittest.TestCase):
    """color
    """
    def test_color_init(self):
        patterns = [Color(), C]
        for pattern in patterns:
            self.assertEqual(pattern.black, 'black')
            self.assertEqual(pattern.white, 'white')
            self.assertEqual(pattern.blank, 'blank')
            self.assertEqual(pattern.colors, ['black', 'white'])
            self.assertEqual(pattern.all, ['black', 'white', 'blank'])

    def test_color_is_black(self):
        c = Color()
        ok = 'black'
        ngs = ['white', 'blank', 'unknown']
        self.assertTrue(c.is_black(ok))
        for ng in ngs:
            self.assertFalse(c.is_black(ng))

    def test_color_is_white(self):
        c = Color()
        ok = 'white'
        ngs = ['black', 'blank', 'unknown']
        self.assertTrue(c.is_white(ok))
        for ng in ngs:
            self.assertFalse(c.is_white(ng))

    def test_color_is_blank(self):
        c = Color()
        ok = 'blank'
        ngs = ['black', 'white', 'unknown']
        self.assertTrue(c.is_blank(ok))
        for ng in ngs:
            self.assertFalse(c.is_blank(ng))

    def test_color_next_color(self):
        c = Color()
        self.assertEqual(c.next_color(c.black), c.white)
        self.assertEqual(c.next_color(c.white), c.black)
        self.assertEqual(c.next_color(c.blank), c.black)
