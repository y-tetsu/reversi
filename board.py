#!/usr/bin/env python
"""
オセロのボード
"""

import abc

from stone import StoneFactory


MIN_BOARD_SIZE = 4   # 最小ボードサイズ
MAX_BOARD_SIZE = 26  # 最大ボードサイズ


class AbstractBoard(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_possibles(self, color):
        pass

    @abc.abstractmethod
    def put_stone(self, color, x, y):
        pass

    @abc.abstractmethod
    def get_board_info(self):
        pass

    @abc.abstractmethod
    def undo(self):
        pass


class BoardSizeError(Exception):
    """
    ボードサイズのエラー
    """
    pass


class Board(AbstractBoard):
    """
    ボードを管理する
    """
    def __init__(self, size=8):
        # ボードサイズの値チェック
        if not(MIN_BOARD_SIZE <= size <= MAX_BOARD_SIZE and size % 2 == 0):
            raise BoardSizeError(str(size) + ' is invalid size!')

        # ボードサイズの初期設定
        self.size = size

        # 石とスコアの初期設定
        self.stone = {}
        self.score = {}
        factory = StoneFactory()

        for color in ('black', 'white', 'blank'):
            self.stone[color] = factory.create(color)
            if color != 'blank':
                self.score[color] = 2

        # 前回の手
        self.prev = {}

        # 盤面の初期設定
        center = size // 2
        self._board = [[self.stone['blank'] for _ in range(size)] for _ in range(size)]
        self._board[center][center-1] = self.stone['black']
        self._board[center-1][center] = self.stone['black']
        self._board[center-1][center-1] = self.stone['white']
        self._board[center][center] = self.stone['white']

    def __str__(self):
        # 列の見出し
        header = '   ' + ' '.join([chr(97 + i) for i in range(self.size)]) + '\n'

        # 行の見出し+盤面
        body = ''

        for num, row in enumerate(self._board, 1):
            body += f'{num:2d}' + ''.join([value for value in row]) + '\n'

        return header + body

    def get_possibles(self, color):
        """
        石が置ける場所をすべて返す
        """
        ret = {}

        for y in range(self.size):
            for x in range(self.size):
                reversibles = self._get_reversibles(color, x, y)

                if reversibles:
                    ret[(x, y)] = reversibles

        return ret

    def _get_reversibles(self, color, x, y):
        """
        指定座標のひっくり返せる石の場所をすべて返す
        """
        directions = [
            (1, 0), (1, 1), (0, 1), (-1, 1),
            (-1, 0), (-1, -1), (0, -1), (1, -1)
        ]
        ret = []

        # 指定座標が範囲内 かつ 石が置いていない
        if self._in_range(x, y) and self._board[y][x] == self.stone['blank']:
            # 8方向をチェック
            for direction in directions:
                tmp = self._get_reversibles_in_direction(color, x, y, direction)

                if tmp:
                    ret += tmp

        return ret

    def _get_reversibles_in_direction(self, color, x, y, direction):
        """
        指定座標から指定方向に向けてひっくり返せる石の場所を返す
        """
        ret = []
        next_x, next_y = x, y
        dx, dy = direction

        while True:
            next_x, next_y = next_x + dx, next_y + dy

            # 座標が範囲内
            if self._in_range(next_x, next_y):
                next_value = self._board[next_y][next_x]

                # 石が置いていない
                if next_value != self.stone['blank']:
                    # 置いた石と同じ色が見つかった場合
                    if next_value == self.stone[color]:
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

    def put_stone(self, color, x, y):
        """
        指定座標に石を置いて返せる場所をひっくり返し、取れた石の座標を返す
        """
        possibles = self.get_possibles(color)

        if (x, y) in possibles:
            self._board[y][x] = self.stone[color]  # 指定座標に指定した色の石を置く
            reversibles = possibles[(x, y)]

            # ひっくり返せる場所に指定した色の石を変更する
            for tmp_x, tmp_y, in reversibles:
                self._board[tmp_y][tmp_x] = self.stone[color]

            self._update_stone_num()

            # 打った手の記録
            self.prev = {'color': color, 'x': x, 'y': y, 'reversibles': reversibles}

            return reversibles

        return []

    def _update_stone_num(self):
        """
        石の数を更新する
        """
        for color in ('black', 'white'):
            self.score[color] = sum([row.count(self.stone[color]) for row in self._board])

    def get_board_info(self):
        """
        ボードの情報を返す
        """
        board_info = []

        for row in self._board:
            tmp = []

            for col in row:
                if col == self.stone['black']:
                    tmp.append(1)
                elif col == self.stone['white']:
                    tmp.append(-1)
                elif col == self.stone['blank']:
                    tmp.append(0)

            board_info.append(tmp)

        return board_info

    def undo(self):
        """
        やり直し
        """
        if self.prev:
            color = self.prev['color']
            prev_color = 'white' if color == 'black' else 'black'
            x = self.prev['x']
            y = self.prev['y']
            reversibles = self.prev['reversibles']
            self._board[y][x] = self.stone['blank']

            for prev_x, prev_y in reversibles:
                self._board[prev_y][prev_x] = self.stone[prev_color]


class BitBoard(AbstractBoard):
    """
    ボードを管理する(ビットボードによる実装)
    """
    def __init__(self, size=8):
        # ボードサイズの値チェック
        if not(MIN_BOARD_SIZE <= size <= MAX_BOARD_SIZE and size % 2 == 0):
            raise BoardSizeError(str(size) + ' is invalid size!')

        # ボードサイズの初期設定
        self.size = size

        # 石とスコアの初期設定
        self.stone = {}
        self.score = {}
        factory = StoneFactory()

        for color in ('black', 'white', 'blank'):
            self.stone[color] = factory.create(color)
            if color != 'blank':
                self.score[color] = 2

        # 前回の手
        self.prev = {}

        # 盤面の初期設定
        center = size // 2
        self._board = [[self.stone['blank'] for _ in range(size)] for _ in range(size)]
        self._board[center][center-1] = self.stone['black']
        self._board[center-1][center] = self.stone['black']
        self._board[center-1][center-1] = self.stone['white']
        self._board[center][center] = self.stone['white']

        # ビットボードの情報
        black_bitboard_list = (['0'] * size) * size
        white_bitboard_list = (['0'] * size) * size
        max_bitboard_list = (['1'] * size) * size

        black_bitboard_list[size*(center-1)+center] = '1'
        black_bitboard_list[size*center+(center-1)] = '1'
        white_bitboard_list[size*(center-1)+(center-1)] = '1'
        white_bitboard_list[size*center+center] = '1'

        self._black_bitboard = int(''.join(black_bitboard_list), 2)
        self._white_bitboard = int(''.join(white_bitboard_list), 2)
        self._max_bitboard = int(''.join(max_bitboard_list), 2)

        self._bitboard_size = size * size
        check = 16

        while self._bitboard_size > check:
            check *= 2

        self._bitboard_size = check

    def __str__(self):
        pass

    def _is_board_full(self):
        """
        石が置けるか
        """
        return not (~(self._black_bitboard | self._white_bitboard) & self._max_bitboard)

    def _num_of_stones(self, stones):
        """
        石の数を数える
        """
        mask = int(''.join(['5'] * (self._bitboard_size // 4)), 16)
        stones = stones - (stones >> 1 & mask)

        mask = int(''.join(['3'] * (self._bitboard_size // 4)), 16)
        stones = (stones & mask) + (stones >> 2 & mask)

        check = 4
        while check <= self._bitboard_size // 2:
            mask = int(''.join((['0'] * (check // 4) + ['F'] * (check // 4)) * (self._bitboard_size // 2 // check)), 16)
            stones = (stones & mask) + (stones >> check & mask)
            print(f'mask 0x{mask:x}')
            check *= 2

        return stones

    def get_possibles(self, color):
        """
        石が置ける場所をすべて返す
        """
        pass

    def put_stone(self, color, x, y):
        """
        指定座標に石を置いて返せる場所をひっくり返し、取れた石の座標を返す
        """
        pass

    def get_board_info(self):
        """
        ボードの情報を返す
        """
        pass

    def undo(self):
        """
        やり直し
        """
        pass


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
    board4_ini = [[board4.stone['blank'] for _ in range(4)] for _ in range(4)]
    board4_ini[2][1] = board4.stone['black']
    board4_ini[1][2] = board4.stone['black']
    board4_ini[1][1] = board4.stone['white']
    board4_ini[2][2] = board4.stone['white']
    assert board4._board == board4_ini

    print(board6)
    board6_ini = [[board6.stone['blank'] for _ in range(6)] for _ in range(6)]
    board6_ini[3][2] = board6.stone['black']
    board6_ini[2][3] = board6.stone['black']
    board6_ini[2][2] = board6.stone['white']
    board6_ini[3][3] = board6.stone['white']
    assert board6._board == board6_ini

    print(board8)
    board8_ini = [[board8.stone['blank'] for _ in range(8)] for _ in range(8)]
    board8_ini[4][3] = board8.stone['black']
    board8_ini[3][4] = board8.stone['black']
    board8_ini[3][3] = board8.stone['white']
    board8_ini[4][4] = board8.stone['white']
    assert board8._board == board8_ini

    print(board10)
    board10_ini = [[board10.stone['blank'] for _ in range(10)] for _ in range(10)]
    board10_ini[5][4] = board10.stone['black']
    board10_ini[4][5] = board10.stone['black']
    board10_ini[4][4] = board10.stone['white']
    board10_ini[5][5] = board10.stone['white']
    assert board10._board == board10_ini

    print(board26)
    board26_ini = [[board26.stone['blank'] for _ in range(26)] for _ in range(26)]
    board26_ini[13][12] = board26.stone['black']
    board26_ini[12][13] = board26.stone['black']
    board26_ini[12][12] = board26.stone['white']
    board26_ini[13][13] = board26.stone['white']
    assert board26._board == board26_ini

    # 石を置く
    assert board4.put_stone('black', 0, 0) == []
    assert board4.put_stone('black', 3, 5) == []
    assert board4.put_stone('black', 1, 0) == [(1, 1)]
    assert board4.put_stone('white', 0, 0) == [(1, 1)]
    assert board4.put_stone('black', 0, 1) == [(1, 1)]
    assert board4.put_stone('white', 2, 0) == [(2, 1), (1, 0)]
    assert board4.put_stone('black', 3, 0) == [(2, 1)]
    assert board4.put_stone('white', 1, 3) == [(1, 2), (1, 1)]
    assert board4.put_stone('black', 0, 3) == [(1, 2)]
    assert board4.put_stone('white', 0, 2) == [(1, 2), (0, 1)]
    assert board4.put_stone('black', 2, 3) == [(1, 3), (2, 2)]
    assert board4.put_stone('white', 3, 2) == [(2, 2), (2, 1)]
    assert board4.put_stone('black', 3, 1) == [(2, 2)]
    assert board4.put_stone('white', 3, 3) == [(2, 2)]

    # プレイ結果
    print(board4)
    board4_ret = [[board4.stone['blank'] for _ in range(4)] for _ in range(4)]
    board4_ret[0][0] = board4.stone['white']
    board4_ret[0][1] = board4.stone['white']
    board4_ret[0][2] = board4.stone['white']
    board4_ret[0][3] = board4.stone['black']
    board4_ret[1][0] = board4.stone['white']
    board4_ret[1][1] = board4.stone['white']
    board4_ret[1][2] = board4.stone['white']
    board4_ret[1][3] = board4.stone['black']
    board4_ret[2][0] = board4.stone['white']
    board4_ret[2][1] = board4.stone['white']
    board4_ret[2][2] = board4.stone['white']
    board4_ret[2][3] = board4.stone['white']
    board4_ret[3][0] = board4.stone['black']
    board4_ret[3][1] = board4.stone['black']
    board4_ret[3][2] = board4.stone['black']
    board4_ret[3][3] = board4.stone['white']
    assert board4._board == board4_ret
    assert board4.score['black'] == 5
    assert board4.score['white'] == 11

    print(board4.get_board_info())

    # やり直し
    board4 = Board(4)
    board4.put_stone('black', 0, 1)
    print(board4)
    board4.undo()
    print(board4)
    board4.put_stone('white', 0, 2)
    print(board4)
    board4.undo()
    print(board4)

    # ビットボード
    bitboard4 = BitBoard(4)
    bitboard8 = BitBoard(8)
    bitboard10 = BitBoard(10)
    bitboard20 = BitBoard(20)
    bitboard26 = BitBoard(26)

    print(f'0x{bitboard4._black_bitboard:x}')
    assert bitboard4._black_bitboard == 0x240

    print(f'0x{bitboard4._white_bitboard:x}')
    assert bitboard4._white_bitboard == 0x420

    print(f'0x{bitboard8._black_bitboard:x}')
    assert bitboard8._black_bitboard == 0x810000000

    print(f'0x{bitboard8._white_bitboard:x}')
    assert bitboard8._white_bitboard == 0x1008000000

    bitboard4._black_bitboard = 0x5555
    bitboard4._white_bitboard = 0xAAAA
    assert bitboard4._is_board_full()

    bitboard4._black_bitboard = 0x0
    bitboard4._white_bitboard = 0xF
    assert not bitboard4._is_board_full()

    bitboard4._black_bitboard = 0x00
    bitboard4._white_bitboard = 0xFF
    assert not bitboard4._is_board_full()

    bitboard4._black_bitboard = 0x000
    bitboard4._white_bitboard = 0xFFF
    assert not bitboard4._is_board_full()

    bitboard4._black_bitboard = 0x0000
    bitboard4._white_bitboard = 0xFFFF
    assert bitboard4._is_board_full()

    assert bitboard4._bitboard_size == 16
    assert bitboard8._bitboard_size == 64
    assert bitboard10._bitboard_size == 128
    assert bitboard20._bitboard_size == 512
    assert bitboard26._bitboard_size == 1024

    print(bitboard4._num_of_stones(bitboard4._white_bitboard))

    bitboard8._black_bitboard = 0x5555555555555555
    print(bitboard8._num_of_stones(bitboard8._black_bitboard))
