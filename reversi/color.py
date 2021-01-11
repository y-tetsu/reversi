"""Color
"""


class Color:
    """Color"""
    def __init__(self):
        self.black = 'black'
        self.white = 'white'
        self.blank = 'blank'
        self.colors = [self.black, self.white]
        self.all = self.colors + [self.blank]

    def is_black(self, color):
        return color == self.black

    def is_white(self, color):
        return color == self.white

    def is_blank(self, color):
        return color == self.blank

    def next_color(self, color):
        return self.white if color == self.black else self.black


C = Color()
