#!/usr/bin/env python
"""
オセロのボード
"""

from stone import StoneFactory


MIN_BOARD_SIZE = 4
MAX_BOARD_SIZE = 26


class BoardSizeError(Exception):
    """
    ボードサイズのエラー
    """
    pass


class Board:
    """
    ボードを管理する
    """
    def __init__(self, size=8):
        if not(MIN_BOARD_SIZE <= size <= MAX_BOARD_SIZE and size % 2 == 0):
            raise BoardSizeError(str(size) + " is invalid size!")

        self.size = size

        factory = StoneFactory()
        self.black = factory.create('black')
        self.white = factory.create('white')
        self.blank = factory.create('blank')

        self.black_num = 2
        self.white_num = 2

        center = size // 2
        self._board = [[self.blank for _ in range(size)] for _ in range(size)]
        self._board[center][center-1] = self.black
        self._board[center-1][center] = self.black
        self._board[center-1][center-1] = self.white
        self._board[center][center] = self.white

    def __str__(self):
        header = "   " + " ".join([chr(97 + i) for i in range(self.size)]) + "\n"
        body = ""

        for num, row in enumerate(self._board, 1):
            body += f'{num:2d}' + "".join([value for value in row]) + "\n"

        return header + body

    def is_full(self):
        """
        すべてのマスに石が置かれている
        """
        for row in self._board:
            if self.blank in row:
                return False

        return True

    def get_possibles(self, stone):
        """
        石が置ける場所をすべて返す
        """
        ret = {}

        for y in range(self.size):
            for x in range(self.size):
                reversibles = self._get_reversibles(stone, x, y)

                if reversibles:
                    ret[(x, y)] = reversibles

        return ret

    def _get_reversibles(self, stone, x, y):
        """
        指定座標のひっくり返せる石の場所をすべて返す
        """
        directions = [
            (1, 0), (1, 1), (0, 1), (-1, 1),
            (-1, 0), (-1, -1), (0, -1), (1, -1)
        ]
        ret = []

        if self._in_range(x, y) and self._board[y][x] == self.blank:
            for direction in directions:
                tmp = self._get_reversibles_in_direction(stone, x, y, direction)

                if tmp:
                    ret += tmp

        return ret

    def _get_reversibles_in_direction(self, stone, x, y, direction):
        """
        指定座標から指定方向に向けてひっくり返せる石の場所を返す
        """
        ret = []
        next_x, next_y = x, y
        dx, dy = direction

        while True:
            next_x, next_y = next_x + dx, next_y + dy

            if self._in_range(next_x, next_y):
                next_value = self._board[next_y][next_x]

                if next_value != self.blank:
                    if next_value == stone:
                        return ret

                    ret += [(next_x, next_y)]
                else:
                    break
            else:
                break

        return []

    def _in_range(self, x, y):
        """
        座標がボードの範囲内かどうかを返す
        """
        if 0 <= x < self.size and 0 <= y < self.size:
            return True

        return False

    def put(self, stone, x, y):
        """
        指定座標に石を置いて返せる場所をひっくり返し、取れた石の座標を返す
        """
        possibles = self.get_possibles(stone)

        if (x, y) in possibles:
            self._board[y][x] = stone
            reversibles = possibles[(x, y)]

            for tmp_x, tmp_y, in reversibles:
                self._board[tmp_y][tmp_x] = stone

            self._update_stone_num()

            return reversibles

        return []

    def _update_stone_num(self):
        """
        石の数を更新する
        """
        self.black_num = self._count_stone_num(self.black)
        self.white_num = self._count_stone_num(self.white)

    def _count_stone_num(self, stone):
        """
        石の数を数える
        """
        return sum([row.count(stone) for row in self._board])

    def get_board_info(self):
        """
        ボードの情報を返す
        """
        return self._board


if __name__ == '__main__':
    # サイズ異常
    invalid2 = False
    try:
        board2 = Board(2)
    except BoardSizeError as e:
        print(e)
        invalid2 = True

    assert invalid2

    invalid3 = False
    try:
        board3 = Board(3)
    except BoardSizeError as e:
        print(e)
        invalid3 = True

    assert invalid3

    invalid28 = False
    try:
        board28 = Board(28)
    except BoardSizeError as e:
        print(e)
        invalid28 = True

    assert invalid28

    # 初期値
    board4 = Board(4)
    board6 = Board(6)
    board8 = Board()
    board10 = Board(10)
    board26 = Board(26)

    print(board4)
    board4_ini = [[board4.blank for _ in range(4)] for _ in range(4)]
    board4_ini[2][1] = board4.black
    board4_ini[1][2] = board4.black
    board4_ini[1][1] = board4.white
    board4_ini[2][2] = board4.white
    assert board4._board == board4_ini

    print(board6)
    board6_ini = [[board6.blank for _ in range(6)] for _ in range(6)]
    board6_ini[3][2] = board6.black
    board6_ini[2][3] = board6.black
    board6_ini[2][2] = board6.white
    board6_ini[3][3] = board6.white
    assert board6._board == board6_ini

    print(board8)
    board8_ini = [[board8.blank for _ in range(8)] for _ in range(8)]
    board8_ini[4][3] = board8.black
    board8_ini[3][4] = board8.black
    board8_ini[3][3] = board8.white
    board8_ini[4][4] = board8.white
    assert board8._board == board8_ini

    print(board10)
    board10_ini = [[board10.blank for _ in range(10)] for _ in range(10)]
    board10_ini[5][4] = board10.black
    board10_ini[4][5] = board10.black
    board10_ini[4][4] = board10.white
    board10_ini[5][5] = board10.white
    assert board10._board == board10_ini

    print(board26)
    board26_ini = [[board26.blank for _ in range(26)] for _ in range(26)]
    board26_ini[13][12] = board26.black
    board26_ini[12][13] = board26.black
    board26_ini[12][12] = board26.white
    board26_ini[13][13] = board26.white
    assert board26._board == board26_ini

    # 石を置く
    assert board4.put(board4.black, 0, 0) == []
    assert board4.put(board4.black, 3, 5) == []
    assert board4.put(board4.black, 1, 0) == [(1, 1)]
    assert board4.put(board4.white, 0, 0) == [(1, 1)]
    assert board4.put(board4.black, 0, 1) == [(1, 1)]
    assert board4.put(board4.white, 2, 0) == [(2, 1), (1, 0)]
    assert board4.put(board4.black, 3, 0) == [(2, 1)]
    assert board4.put(board4.white, 1, 3) == [(1, 2), (1, 1)]
    assert board4.put(board4.black, 0, 3) == [(1, 2)]
    assert board4.put(board4.white, 0, 2) == [(1, 2), (0, 1)]
    assert board4.put(board4.black, 2, 3) == [(1, 3), (2, 2)]
    assert board4.put(board4.white, 3, 2) == [(2, 2), (2, 1)]
    assert board4.put(board4.black, 3, 1) == [(2, 2)]
    assert board4.put(board4.white, 3, 3) == [(2, 2)]

    # プレイ結果
    print(board4)
    board4_ret = [[board4.blank for _ in range(4)] for _ in range(4)]
    board4_ret[0][0] = board4.white
    board4_ret[0][1] = board4.white
    board4_ret[0][2] = board4.white
    board4_ret[0][3] = board4.black
    board4_ret[1][0] = board4.white
    board4_ret[1][1] = board4.white
    board4_ret[1][2] = board4.white
    board4_ret[1][3] = board4.black
    board4_ret[2][0] = board4.white
    board4_ret[2][1] = board4.white
    board4_ret[2][2] = board4.white
    board4_ret[2][3] = board4.white
    board4_ret[3][0] = board4.black
    board4_ret[3][1] = board4.black
    board4_ret[3][2] = board4.black
    board4_ret[3][3] = board4.white
    assert board4._board == board4_ret
    assert board4.black_num == 5
    assert board4.white_num == 11

    # ボードが一杯かどうか
    assert board4.is_full()

    board4._board[3][3] = board4.blank
    assert not board4.is_full()
