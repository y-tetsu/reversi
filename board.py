#!/usr/bin/env python
"""
オセロのボード
"""

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
    BLACK, WHITE, BLANK = 0, 1, 2
    MARK = {
        BLANK: "□", BLACK: "〇", WHITE: "●"
    }

    def __init__(self, size=8):
        if not(MIN_BOARD_SIZE <= size <= MAX_BOARD_SIZE and size % 2 == 0):
            raise BoardSizeError(str(size) + " is invalid size!")

        self.size = size
        self.black_num = 2
        self.white_num = 2

        center = size // 2
        self._board = [[Board.BLANK for _ in range(size)] for _ in range(size)]
        self._board[center][center-1] = Board.BLACK
        self._board[center-1][center] = Board.BLACK
        self._board[center-1][center-1] = Board.WHITE
        self._board[center][center] = Board.WHITE

    def __str__(self):
        header = "   " + " ".join([chr(97 + i) for i in range(self.size)]) + "\n"
        body = ""

        for num, row in enumerate(self._board, 1):
            body += f'{num:2d}' + "".join([self.MARK[value] for value in row]) + "\n"

        return header + body

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

        if self._in_range(x, y) and self._board[y][x] == Board.BLANK:
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

                if next_value != Board.BLANK:
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
        self.black_num = self._count_stone_num(Board.BLACK)
        self.white_num = self._count_stone_num(Board.WHITE)

    def _count_stone_num(self, stone):
        """
        石の数を数える
        """
        return sum([row.count(stone) for row in self._board])


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
    board4_ini = [[Board.BLANK for _ in range(4)] for _ in range(4)]
    board4_ini[2][1] = Board.BLACK
    board4_ini[1][2] = Board.BLACK
    board4_ini[1][1] = Board.WHITE
    board4_ini[2][2] = Board.WHITE
    assert board4._board == board4_ini

    print(board6)
    board6_ini = [[Board.BLANK for _ in range(6)] for _ in range(6)]
    board6_ini[3][2] = Board.BLACK
    board6_ini[2][3] = Board.BLACK
    board6_ini[2][2] = Board.WHITE
    board6_ini[3][3] = Board.WHITE
    assert board6._board == board6_ini

    print(board8)
    board8_ini = [[Board.BLANK for _ in range(8)] for _ in range(8)]
    board8_ini[4][3] = Board.BLACK
    board8_ini[3][4] = Board.BLACK
    board8_ini[3][3] = Board.WHITE
    board8_ini[4][4] = Board.WHITE
    assert board8._board == board8_ini

    print(board10)
    board10_ini = [[Board.BLANK for _ in range(10)] for _ in range(10)]
    board10_ini[5][4] = Board.BLACK
    board10_ini[4][5] = Board.BLACK
    board10_ini[4][4] = Board.WHITE
    board10_ini[5][5] = Board.WHITE
    assert board10._board == board10_ini

    print(board26)
    board26_ini = [[Board.BLANK for _ in range(26)] for _ in range(26)]
    board26_ini[13][12] = Board.BLACK
    board26_ini[12][13] = Board.BLACK
    board26_ini[12][12] = Board.WHITE
    board26_ini[13][13] = Board.WHITE
    assert board26._board == board26_ini

    # 石を置く
    assert board4.put(Board.BLACK, 0, 0) == []
    assert board4.put(Board.BLACK, 3, 5) == []
    assert board4.put(Board.BLACK, 1, 0) == [(1, 1)]
    assert board4.put(Board.WHITE, 0, 0) == [(1, 1)]
    assert board4.put(Board.BLACK, 0, 1) == [(1, 1)]
    assert board4.put(Board.WHITE, 2, 0) == [(2, 1), (1, 0)]
    assert board4.put(Board.BLACK, 3, 0) == [(2, 1)]
    assert board4.put(Board.WHITE, 1, 3) == [(1, 2), (1, 1)]
    assert board4.put(Board.BLACK, 0, 3) == [(1, 2)]
    assert board4.put(Board.WHITE, 0, 2) == [(1, 2), (0, 1)]
    assert board4.put(Board.BLACK, 2, 3) == [(1, 3), (2, 2)]
    assert board4.put(Board.WHITE, 3, 2) == [(2, 2), (2, 1)]
    assert board4.put(Board.BLACK, 3, 1) == [(2, 2)]
    assert board4.put(Board.WHITE, 3, 3) == [(2, 2)]

    # プレイ結果
    print(board4)
    board4_ret = [[Board.BLANK for _ in range(4)] for _ in range(4)]
    board4_ret[0][0] = Board.WHITE
    board4_ret[0][1] = Board.WHITE
    board4_ret[0][2] = Board.WHITE
    board4_ret[0][3] = Board.BLACK
    board4_ret[1][0] = Board.WHITE
    board4_ret[1][1] = Board.WHITE
    board4_ret[1][2] = Board.WHITE
    board4_ret[1][3] = Board.BLACK
    board4_ret[2][0] = Board.WHITE
    board4_ret[2][1] = Board.WHITE
    board4_ret[2][2] = Board.WHITE
    board4_ret[2][3] = Board.WHITE
    board4_ret[3][0] = Board.BLACK
    board4_ret[3][1] = Board.BLACK
    board4_ret[3][2] = Board.BLACK
    board4_ret[3][3] = Board.WHITE
    assert board4._board == board4_ret
    assert board4.black_num == 5
    assert board4.white_num == 11
