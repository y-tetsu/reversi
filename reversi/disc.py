#!/usr/bin/env python
"""
石の管理
"""


class Disc(str):
    """
    石の基底クラス
    """
    __slots__ = ()  # データを持たない


class Black(Disc):
    pass


class White(Disc):
    pass


class Blank(Disc):
    pass


class DiscFactory:
    """
    石ファクトリ
    """
    def create(self, color):
        """
        石オブジェクトを生成する
        """
        ret = ''

        if color == 'black':
            ret = Black('〇')
        elif color == 'white':
            ret = White('●')
        elif color == 'blank':
            ret = Blank('□')

        return ret
