#!/usr/bin/env python
"""
オセロの石
"""


BLACK, WHITE, BLANK = (("BLACK", "〇"), ("WHITE", "●"), ("BLANK", "□"))


class StoneFactory:
    """
    石ファクトリ
    """
    def __init__(self):
        # 黒、白、空クラス生成
        for color, mark in (BLACK, WHITE, BLANK):
            new = (lambda m: lambda Class: Stone.__new__(Class, m))(mark)
            new.__name__ = "__new__"  # クラスに使うので名前を<lambda>から__new__へ変更
            Class = type(color.title(), (Stone,), dict(__slots__=(), __new__=new))
            globals()[color.title()] = Class

    def create(self, color):
        """
        石オブジェクトを生成する
        """
        return globals()[color.title()]()


class Stone(str):
    """
    石の基底クラス
    """
    __slots__ = ()  # データを持たない


if __name__ == '__main__':
    from collections import namedtuple

    factory = StoneFactory()

    CheckStone = namedtuple('CheckStone', 'color cls mark')
    black = CheckStone('black', Black, "〇")
    white = CheckStone('white', White, "●")
    blank = CheckStone('blank', Blank, "□")

    for check in (black, white, blank):
        obj = factory.create(check.color)
        print(obj)
        assert isinstance(obj, check.cls)
        assert obj == check.mark
