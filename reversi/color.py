"""Color
"""


class Color:
    """Color"""
    def __init__(self):
        self.__green = 'green'
        self.__black = 'black'
        self.__white = 'white'
        self.__blank = 'blank'
        self.__hole = 'hole'
        self.__colors = [self.__green, self.__black, self.__white]
        self.__all = self.colors + [self.__blank, self.__hole]

    @property
    def green(self):
        return self.__green

    @property
    def black(self):
        return self.__black

    @property
    def white(self):
        return self.__white

    @property
    def blank(self):
        return self.__blank

    @property
    def hole(self):
        return self.__hole

    @property
    def colors(self):
        return self.__colors

    @property
    def all(self):
        return self.__all

    def is_green(self, color):
        return color == self.__green

    def is_black(self, color):
        return color == self.__black

    def is_white(self, color):
        return color == self.__white

    def is_blank(self, color):
        return color == self.__blank

    def is_hole(self, color):
        return color == self.__hole

    def next_color(self, color):
        return self.__white if color == self.__black else self.__black


C = Color()
