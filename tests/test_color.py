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

    def test_color_next_color(self):
        c = Color()
        self.assertEqual(c.next_color(c.black), c.white)
        self.assertEqual(c.next_color(c.white), c.black)
        self.assertEqual(c.next_color(c.blank), c.black)
