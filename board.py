#!/usr/bin/env python
"""
オセロのボード
"""


class BoardSizeError(Exception):
    pass


class Board:
    """
    ボードを管理する
    """
    BLACK, WHITE, BLANK = 0, 1, 2

    def __init__(self, size=4):
        self.size = size
        self.directions = [
            (1, 0), (1, 1), (0, 1), (-1, 1),
            (-1, 0), (-1, -1), (0, -1), (1, -1)
        ]

        if size < 4 or size % 2:
            raise BoardSizeError(str(size) + " is invalid size!")

        self.board = [[Board.BLANK for _ in range(size)] for _ in range(size)]
        center = size // 2

        self.board[center][center-1] = Board.BLACK
        self.board[center-1][center] = Board.BLACK
        self.board[center-1][center-1] = Board.WHITE
        self.board[center][center] = Board.WHITE

        self.black_num = 2
        self.white_num = 2

    def print_board(self):
        """
        コンソールにボードを表示する
        """
        print("BLACK :", self.black_num, "WHITE :", self.white_num)

        for row in self.board:
            for val in row:
                if val == Board.BLANK:
                    print("□", end="")
                elif val == Board.BLACK:
                    print("〇", end="")
                elif val == Board.WHITE:
                    print("●", end="")
            print()

        print()

    def count_stone(self):
        """
        石の数を数える
        """
        self.black_num = sum([row.count(Board.BLACK) for row in self.board])
        self.white_num = sum([row.count(Board.WHITE) for row in self.board])

        return self.black_num, self.white_num

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

        if self.in_range(x, y) and self.board[y][x] == Board.BLANK:
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

                if next_value != Board.BLANK:
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
        指定座標に石を置いて返せる場所をひっくり返し、取れた数を返す
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
    board4_ini = [[Board.BLANK for _ in range(4)] for _ in range(4)]
    board4_ini[2][1] = Board.BLACK
    board4_ini[1][2] = Board.BLACK
    board4_ini[1][1] = Board.WHITE
    board4_ini[2][2] = Board.WHITE
    assert board4.board == board4_ini

    board6.print_board()
    board6_ini = [[Board.BLANK for _ in range(6)] for _ in range(6)]
    board6_ini[3][2] = Board.BLACK
    board6_ini[2][3] = Board.BLACK
    board6_ini[2][2] = Board.WHITE
    board6_ini[3][3] = Board.WHITE
    assert board6.board == board6_ini

    board8.print_board()
    board8_ini = [[Board.BLANK for _ in range(8)] for _ in range(8)]
    board8_ini[4][3] = Board.BLACK
    board8_ini[3][4] = Board.BLACK
    board8_ini[3][3] = Board.WHITE
    board8_ini[4][4] = Board.WHITE
    assert board8.board == board8_ini

    board10.print_board()
    board10_ini = [[Board.BLANK for _ in range(10)] for _ in range(10)]
    board10_ini[5][4] = Board.BLACK
    board10_ini[4][5] = Board.BLACK
    board10_ini[4][4] = Board.WHITE
    board10_ini[5][5] = Board.WHITE
    assert board10.board == board10_ini

    # 石を置く
    assert board4.put_stone(0, 0, Board.BLACK) == 0
    assert board4.put_stone(3, 5, Board.BLACK) == 0
    assert board4.put_stone(1, 0, Board.BLACK) == 1
    assert board4.put_stone(0, 0, Board.WHITE) == 1
    assert board4.put_stone(0, 1, Board.BLACK) == 1
    assert board4.put_stone(2, 0, Board.WHITE) == 2
    assert board4.put_stone(3, 0, Board.BLACK) == 1
    assert board4.put_stone(1, 3, Board.WHITE) == 2
    assert board4.put_stone(0, 3, Board.BLACK) == 1
    assert board4.put_stone(0, 2, Board.WHITE) == 2
    assert board4.put_stone(2, 3, Board.BLACK) == 2
    assert board4.put_stone(3, 2, Board.WHITE) == 2
    assert board4.put_stone(3, 1, Board.BLACK) == 1
    assert board4.put_stone(3, 3, Board.WHITE) == 1

    # プレイ結果
    board4.print_board()
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
    assert board4.board == board4_ret
    assert board4.black_num == 5
    assert board4.white_num == 11