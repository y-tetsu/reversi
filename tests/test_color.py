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
            self.assertEqual(pattern.green, 'green')
            self.assertEqual(pattern.black, 'black')
            self.assertEqual(pattern.white, 'white')
            self.assertEqual(pattern.blank, 'blank')
            self.assertEqual(pattern.hole, 'hole')
            self.assertEqual(pattern.colors, ['green', 'black', 'white'])
            self.assertEqual(pattern.all, ['green', 'black', 'white', 'blank', 'hole'])

    def test_color_is_green(self):
        c = Color()
        ok = 'green'
        ngs = ['black', 'white', 'blank', 'hole', 'unknown']
        self.assertTrue(c.is_green(ok))
        for ng in ngs:
            self.assertFalse(c.is_green(ng))

    def test_color_is_black(self):
        c = Color()
        ok = 'black'
        ngs = ['green', 'white', 'blank', 'hole', 'unknown']
        self.assertTrue(c.is_black(ok))
        for ng in ngs:
            self.assertFalse(c.is_black(ng))

    def test_color_is_white(self):
        c = Color()
        ok = 'white'
        ngs = ['green', 'black', 'blank', 'hole', 'unknown']
        self.assertTrue(c.is_white(ok))
        for ng in ngs:
            self.assertFalse(c.is_white(ng))

    def test_color_is_blank(self):
        c = Color()
        ok = 'blank'
        ngs = ['green', 'black', 'white', 'hole', 'unknown']
        self.assertTrue(c.is_blank(ok))
        for ng in ngs:
            self.assertFalse(c.is_blank(ng))

    def test_color_is_hole(self):
        c = Color()
        ok = 'hole'
        ngs = ['green', 'black', 'white', 'blank', 'unknown']
        self.assertTrue(c.is_hole(ok))
        for ng in ngs:
            self.assertFalse(c.is_hole(ng))

    def test_color_next_color(self):
        c = Color()
        self.assertEqual(c.next_color(c.green), c.black)
        self.assertEqual(c.next_color(c.black), c.white)
        self.assertEqual(c.next_color(c.white), c.black)
        self.assertEqual(c.next_color(c.blank), c.black)
        self.assertEqual(c.next_color(c.hole), c.black)

    def test_color_property(self):
        c = Color()
        with self.assertRaises(AttributeError):
            c.green = 'another color'
        with self.assertRaises(AttributeError):
            c.black = 'another color'
        with self.assertRaises(AttributeError):
            c.white = 'another color'
        with self.assertRaises(AttributeError):
            c.blank = 'another color'
        with self.assertRaises(AttributeError):
            c.hole = 'another color'
        with self.assertRaises(AttributeError):
            c.colors = []
        with self.assertRaises(AttributeError):
            c.all = []
