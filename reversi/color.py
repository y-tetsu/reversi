"""Color
"""


class Color:
    """Color"""
    def __init__(self):
        self.black = 'black'
        self.white = 'white'
        self.blank = 'blank'
        self.colors = [self.black, self.white]
        self.all = [self.black, self.white, self.blank]

    def next_color(self, color):
        return self.white if color == self.black else self.black


C = Color()
