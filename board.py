#!/usr/bin/env python
"""
オセロのボード
"""

BLACK, WHITE, BLANK = 0, 1, 2


class BoardSizeError(Exception):
    pass


class Board:
    """
    ボードを管理する
    """
    def __init__(self, size=4):
        self.size = size
        self.directions = [
            (1, 0), (1, 1), (0, 1), (-1, 1),
            (-1, 0), (-1, -1), (0, -1), (1, -1)
        ]

        if size < 4 or size % 2:
            raise BoardSizeError(str(size) + " is invalid size!")

        self.board = [[BLANK for _ in range(size)] for _ in range(size)]
        center = size // 2

        self.board[center][center-1] = BLACK
        self.board[center-1][center] = BLACK
        self.board[center-1][center-1] = WHITE
        self.board[center][center] = WHITE

        self.black = 2
        self.white = 2

    def print_board(self):
        """
        コンソールにボードを表示する
        """
        print("BLACK :", self.black, "WHITE :", self.white)

        for row in self.board:
            for val in row:
                if val == BLANK:
                    print("□", end="")
                elif val == BLACK:
                    print("〇", end="")
                elif val == WHITE:
                    print("●", end="")
            print()

        print()

    def count_stone(self):
        """
        石の数を数える
        """
        self.black = sum([row.count(BLACK) for row in self.board])
        self.white = sum([row.count(WHITE) for row in self.board])

        return self.black, self.white

    def in_range(self, x, y):
        """
        座標がボードの範囲内かどうかを返す
        """
        if 0 <= x < self.size and 0 <= y < self.size:
            return True

        return False

    def get_possibles(self, stone):
        """
        石が置ける場所をすべて返す
        """
        ret = {}

        for y in range(self.size):
            for x in range(self.size):
                reversibles = self.get_reversibles(x, y, stone)

                if reversibles:
                    ret[(x, y)] = reversibles

        return ret

    def get_reversibles(self, x, y, stone):
        """
        指定座標のひっくり返せる石の場所をすべて返す
        """
        ret = []

        if self.in_range(x, y) and self.board[y][x] == BLANK:
            for dx, dy in self.directions:
                tmp = self.get_reversibles_by_direction(x, y, dx, dy, stone)

                if tmp:
                    ret += tmp

        return ret

    def get_reversibles_by_direction(self, x, y, dx, dy, stone):
        """
        指定座標から指定方向に向けてひっくり返せる石の場所を返す
        """
        ret = []
        next_x, next_y = x, y

        while True:
            next_x, next_y = next_x + dx, next_y + dy

            if self.in_range(next_x, next_y):
                next_value = self.board[next_y][next_x]

                if next_value != BLANK:
                    if next_value == stone:
                        return ret

                    ret += [(next_x, next_y)]
                else:
                    break
            else:
                break

        return []

    def put_stone(self, x, y, stone):
        """
        指定座標に石を置いてひっくり返し、その数を返す
        """
        possibles = self.get_possibles(stone)

        if (x, y) in possibles:
            self.board[y][x] = stone
            reversibles = possibles[(x, y)]

            for tmp_x, tmp_y, in reversibles:
                self.board[tmp_y][tmp_x] = stone

            self.count_stone()

            return len(reversibles)

        return 0


if __name__ == '__main__':
    board4 = Board()
    board6 = Board(6)
    board8 = Board(8)
    board10 = Board(10)

    # サイズ異常
    invalid3 = False
    try:
        board3 = Board(3)
    except BoardSizeError as e:
        print(e)
        invalid3 = True

    assert invalid3

    invalid2 = False
    try:
        board2 = Board(2)
    except BoardSizeError as e:
        print(e)
        invalid2 = True

    assert invalid2

    print()

    # 初期値
    board4.print_board()
    board4_ini = [[BLANK for _ in range(4)] for _ in range(4)]
    board4_ini[2][1] = BLACK
    board4_ini[1][2] = BLACK
    board4_ini[1][1] = WHITE
    board4_ini[2][2] = WHITE
    assert board4.board == board4_ini

    board6.print_board()
    board6_ini = [[BLANK for _ in range(6)] for _ in range(6)]
    board6_ini[3][2] = BLACK
    board6_ini[2][3] = BLACK
    board6_ini[2][2] = WHITE
    board6_ini[3][3] = WHITE
    assert board6.board == board6_ini

    board8.print_board()
    board8_ini = [[BLANK for _ in range(8)] for _ in range(8)]
    board8_ini[4][3] = BLACK
    board8_ini[3][4] = BLACK
    board8_ini[3][3] = WHITE
    board8_ini[4][4] = WHITE
    assert board8.board == board8_ini

    board10.print_board()
    board10_ini = [[BLANK for _ in range(10)] for _ in range(10)]
    board10_ini[5][4] = BLACK
    board10_ini[4][5] = BLACK
    board10_ini[4][4] = WHITE
    board10_ini[5][5] = WHITE
    assert board10.board == board10_ini

    # 石を置く
    assert board4.put_stone(0, 0, BLACK) == 0
    assert board4.put_stone(3, 5, BLACK) == 0
    assert board4.put_stone(1, 0, BLACK) == 1
    assert board4.put_stone(0, 0, WHITE) == 1
    assert board4.put_stone(0, 1, BLACK) == 1
    assert board4.put_stone(2, 0, WHITE) == 2
    assert board4.put_stone(3, 0, BLACK) == 1
    assert board4.put_stone(1, 3, WHITE) == 2
    assert board4.put_stone(0, 3, BLACK) == 1
    assert board4.put_stone(0, 2, WHITE) == 2
    assert board4.put_stone(2, 3, BLACK) == 2
    assert board4.put_stone(3, 2, WHITE) == 2
    assert board4.put_stone(3, 1, BLACK) == 1
    assert board4.put_stone(3, 3, WHITE) == 1

    # プレイ結果
    board4.print_board()
    board4_ret = [[BLANK for _ in range(4)] for _ in range(4)]
    board4_ret[0][0] = WHITE
    board4_ret[0][1] = WHITE
    board4_ret[0][2] = WHITE
    board4_ret[0][3] = BLACK
    board4_ret[1][0] = WHITE
    board4_ret[1][1] = WHITE
    board4_ret[1][2] = WHITE
    board4_ret[1][3] = BLACK
    board4_ret[2][0] = WHITE
    board4_ret[2][1] = WHITE
    board4_ret[2][2] = WHITE
    board4_ret[2][3] = WHITE
    board4_ret[3][0] = BLACK
    board4_ret[3][1] = BLACK
    board4_ret[3][2] = BLACK
    board4_ret[3][3] = WHITE
    assert board4.board == board4_ret
