"""Color
"""


class Color:
    """Color"""
    def __init__(self):
        self.__black = 'black'
        self.__white = 'white'
        self.__blank = 'blank'
        self.__colors = [self.__black, self.__white]
        self.__all = self.colors + [self.__blank]

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
    def colors(self):
        return self.__colors

    @property
    def all(self):
        return self.__all

    def is_black(self, color):
        return color == self.__black

    def is_white(self, color):
        return color == self.__white

    def is_blank(self, color):
        return color == self.__blank

    def next_color(self, color):
        return self.__white if color == self.__black else self.__black


C = Color()
