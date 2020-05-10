#!/usr/bin/env python
"""
ボードの管理
"""

import abc
from collections import namedtuple

from reversi.disc import DiscFactory
import reversi.BitBoardMethods as BitBoardMethods


MIN_BOARD_SIZE = 4   # 最小ボードサイズ
MAX_BOARD_SIZE = 26  # 最大ボードサイズ


class AbstractBoard(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_legal_moves(self, color):
        pass

    @abc.abstractmethod
    def put_disc(self, color, x, y):
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
        self.disc = {}
        self.score = {}
        factory = DiscFactory()

        for color in ('black', 'white', 'blank'):
            self.disc[color] = factory.create(color)
            if color != 'blank':
                self.score[color] = 2

        # 前回の手
        self.prev = []

        # 盤面の初期設定
        center = size // 2
        self._board = [[self.disc['blank'] for _ in range(size)] for _ in range(size)]
        self._board[center][center-1] = self.disc['black']
        self._board[center-1][center] = self.disc['black']
        self._board[center-1][center-1] = self.disc['white']
        self._board[center][center] = self.disc['white']

        # 置ける場所のキャッシュ
        self._legal_moves_cache = {}

    def __str__(self):
        # 列の見出し
        header = '   ' + ' '.join([chr(97 + i) for i in range(self.size)]) + '\n'

        # 行の見出し+盤面
        body = ''

        for num, row in enumerate(self._board, 1):
            body += f'{num:2d}' + ''.join([value for value in row]) + '\n'

        return header + body

    def get_legal_moves(self, color, force=False):
        """
        石が置ける場所をすべて返す
        """
        # キャッシュが存在する場合
        if not force and color in self._legal_moves_cache:
            return self._legal_moves_cache[color]

        self._legal_moves_cache.clear()
        legal_moves = {}

        for y in range(self.size):
            for x in range(self.size):
                flippable_discs = self._get_flippable_discs(color, x, y)

                if flippable_discs:
                    legal_moves[(x, y)] = flippable_discs

        self._legal_moves_cache[color] = legal_moves

        return legal_moves

    def _get_flippable_discs(self, color, x, y):
        """
        指定座標のひっくり返せる石の場所をすべて返す
        """
        # 方向
        # (-1,  1) (0,  1) (1,  1)
        # (-1,  0)         (1,  0)
        # (-1, -1) (0, -1) (1, -1)
        directions = [
            (-1,  1), (0,  1), (1,  1),
            (-1,  0),          (1,  0),
            (-1, -1), (0, -1), (1, -1)
        ]
        ret = []

        # 指定座標が範囲内 かつ 石が置いていない
        if self._in_range(x, y) and self._board[y][x] == self.disc['blank']:
            # 8方向をチェック
            for direction in directions:
                tmp = self._get_flippable_discs_in_direction(color, x, y, direction)

                if tmp:
                    ret += tmp

        return ret

    def _get_flippable_discs_in_direction(self, color, x, y, direction):
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

                # 石が置かれている
                if next_value != self.disc['blank']:
                    # 置いた石と同じ色が見つかった場合
                    if next_value == self.disc[color]:
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

    def put_disc(self, color, x, y):
        """
        指定座標に石を置いて返せる場所をひっくり返し、取れた石の座標を返す
        """
        legal_moves = self.get_legal_moves(color)

        if (x, y) in legal_moves:
            self._board[y][x] = self.disc[color]  # 指定座標に指定した色の石を置く
            flippable_discs = legal_moves[(x, y)]

            # ひっくり返せる場所に指定した色の石を変更する
            for tmp_x, tmp_y, in flippable_discs:
                self._board[tmp_y][tmp_x] = self.disc[color]

            self._update_score()

            # 打った手の記録
            self.prev.append({'color': color, 'x': x, 'y': y, 'flippable_discs': flippable_discs})

            return flippable_discs

        return []

    def _update_score(self):
        """
        スコアを更新する
        """
        for color in ('black', 'white'):
            self.score[color] = sum([row.count(self.disc[color]) for row in self._board])

    def get_board_info(self):
        """
        ボードの情報を返す
        """
        board_info = []

        for row in self._board:
            tmp = []

            for col in row:
                if col == self.disc['black']:
                    tmp.append(1)
                elif col == self.disc['white']:
                    tmp.append(-1)
                elif col == self.disc['blank']:
                    tmp.append(0)

            board_info.append(tmp)

        return board_info

    def undo(self):
        """
        やり直し
        """
        prev = self.prev.pop()

        if prev:
            color = prev['color']
            prev_color = 'white' if color == 'black' else 'black'
            x = prev['x']
            y = prev['y']
            flippable_discs = prev['flippable_discs']
            self._board[y][x] = self.disc['blank']

            for prev_x, prev_y in flippable_discs:
                self._board[prev_y][prev_x] = self.disc[prev_color]

            self._update_score()

        self._legal_moves_cache.clear()

    def get_bitboard_info(self):
        """
        ビットボードの情報を返す
        """
        size = self.size
        black_bitboard, white_bitboard = 0, 0
        put = 1 << size * size - 1

        for y in range(self.size):
            for x in range(self.size):
                if self._board[y][x] == self.disc['black']:
                    black_bitboard |= put
                if self._board[y][x] == self.disc['white']:
                    white_bitboard |= put
                put >>= 1

        return  black_bitboard, white_bitboard


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
        self.disc, self.score = {}, {}
        factory = DiscFactory()

        for color in ('black', 'white', 'blank'):
            self.disc[color] = factory.create(color)
            if color != 'blank':
                self.score[color] = 2

        # 前回の手
        self.prev = []

        # ビットボードの初期配置
        center = size // 2
        self._black_bitboard = 1 << ((size*size-1)-(size*(center-1)+center))
        self._black_bitboard |= 1 << ((size*size-1)-(size*center+(center-1)))
        self._white_bitboard = 1 << ((size*size-1)-(size*(center-1)+(center-1)))
        self._white_bitboard |= 1 << ((size*size-1)-(size*center+center))

        # 置ける場所の検出用
        BitMask = namedtuple('BitMask', 'h v d u ur r br b bl l ul')
        self._mask = BitMask(
            int(''.join((['0'] + ['1'] * (size-2) + ['0']) * size), 2),                                      # 水平方向のマスク値
            int(''.join(['0'] * size + ['1'] * size * (size-2) + ['0'] * size), 2),                          # 垂直方向のマスク値
            int(''.join(['0'] * size + (['0'] + (['1'] * (size-2)) + ['0']) * (size-2) + ['0'] * size), 2),  # 斜め方向のマスク値
            int(''.join(['1'] * size * (size-1) + ['0'] * size), 2),                                         # 上方向のマスク値
            int(''.join((['0'] + ['1'] * (size-1)) * (size-1) + ['0'] * size), 2),                           # 右上方向のマスク値
            int(''.join((['0'] + ['1'] * (size-1)) * size), 2),                                              # 右方向のマスク値
            int(''.join(['0'] * size + (['0'] + ['1'] * (size-1)) * (size-1)), 2),                           # 右下方向のマスク値
            int(''.join(['0'] * size + ['1'] * size * (size-1)), 2),                                         # 下方向のマスク値
            int(''.join(['0'] * size + (['1'] * (size-1) + ['0']) * (size-1)), 2),                           # 左下方向のマスク値
            int(''.join((['1'] * (size-1) + ['0']) * size), 2),                                              # 左方向のマスク値
            int(''.join((['1'] * (size-1) + ['0']) * (size-1) + ['0'] * size), 2)                            # 左上方向のマスク値
        )

        # 置ける場所のキャッシュ
        self._legal_moves_cache = {}

    def __str__(self):
        size = self.size

        # 列の見出し
        header = '   ' + ' '.join([chr(97 + i) for i in range(size)]) + '\n'

        # 行の見出し+盤面
        board = [[self.disc['blank'] for _ in range(size)] for _ in range(size)]

        mask = 1 << (size * size - 1)
        for y in range(size):
            for x in range(size):
                if self._black_bitboard & mask:
                    board[y][x] = self.disc['black']
                elif self._white_bitboard & mask:
                    board[y][x] = self.disc['white']
                mask >>= 1

        body = ''
        for num, row in enumerate(board, 1):
            body += f'{num:2d}' + ''.join([value for value in row]) + '\n'

        return header + body

    def get_legal_moves(self, color, force=False):
        """
        石が置ける場所をすべて返す
        """
        # キャッシュが存在する場合
        if not force and color in self._legal_moves_cache:
            return self._legal_moves_cache[color]

        self._legal_moves_cache.clear()

        ret = BitBoardMethods.get_legal_moves(color, self.size, self._black_bitboard, self._white_bitboard, self._mask)
        self._legal_moves_cache[color] = ret

        return ret

    def put_disc(self, color, x, y):
        """
        指定座標に石を置いて返せる場所をひっくり返し、取れた石の座標を返す
        """
        legal_moves = self.get_legal_moves(color)

        if (x, y) in legal_moves:
            # 配置位置を整数に変換
            size = self.size
            put = 1 << ((size*size-1)-(y*size+x))

            # 反転位置を整数に変換
            reversibles_list = legal_moves[(x, y)]
            flippable_discs = 0
            for tmp_x, tmp_y in reversibles_list:
                flippable_discs |= 1 << ((size*size-1)-(tmp_y*size+tmp_x))

            # 自分の石を置いて相手の石をひっくり返す
            if color == 'black':
                self._black_bitboard ^= put | flippable_discs
                self._white_bitboard ^= flippable_discs
                self.score['black'] += 1 + len(reversibles_list)
                self.score['white'] -= len(reversibles_list)
            else:
                self._white_bitboard ^= put | flippable_discs
                self._black_bitboard ^= flippable_discs
                self.score['black'] -= len(reversibles_list)
                self.score['white'] += 1 + len(reversibles_list)

            # 打った手の記録
            self.prev.append({'color': color, 'x': x, 'y': y, 'flippable_discs': flippable_discs, 'disc_num': len(reversibles_list)})

            return reversibles_list

        return []

    def get_board_info(self):
        """
        ボードの情報を返す
        """

        return BitBoardMethods.get_board_info(self.size, self._black_bitboard, self._white_bitboard)

    def undo(self):
        """
        やり直し
        """
        prev = self.prev.pop()

        if prev:
            size = self.size
            flippable_discs, disc_num = prev['flippable_discs'], prev['disc_num']

            put = 1 << ((size*size-1)-(prev['y']*size+prev['x']))

            if prev['color'] == 'black':
                self._black_bitboard ^= put | flippable_discs
                self._white_bitboard ^= flippable_discs
                self.score['black'] -= 1 + disc_num
                self.score['white'] += disc_num
            else:
                self._white_bitboard ^= put | flippable_discs
                self._black_bitboard ^= flippable_discs
                self.score['black'] += disc_num
                self.score['white'] -= 1 + disc_num

        self._legal_moves_cache.clear()

    def get_bitboard_info(self):
        """
        ビットボードの情報を返す
        """
        return  self._black_bitboard, self._white_bitboard


if __name__ == '__main__':
    # ========== #
    # 通常ボード #
    # ========== #
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
    board4_ini = [[board4.disc['blank'] for _ in range(4)] for _ in range(4)]
    board4_ini[2][1] = board4.disc['black']
    board4_ini[1][2] = board4.disc['black']
    board4_ini[1][1] = board4.disc['white']
    board4_ini[2][2] = board4.disc['white']
    assert board4._board == board4_ini

    print(board6)
    board6_ini = [[board6.disc['blank'] for _ in range(6)] for _ in range(6)]
    board6_ini[3][2] = board6.disc['black']
    board6_ini[2][3] = board6.disc['black']
    board6_ini[2][2] = board6.disc['white']
    board6_ini[3][3] = board6.disc['white']
    assert board6._board == board6_ini

    print(board8)
    board8_ini = [[board8.disc['blank'] for _ in range(8)] for _ in range(8)]
    board8_ini[4][3] = board8.disc['black']
    board8_ini[3][4] = board8.disc['black']
    board8_ini[3][3] = board8.disc['white']
    board8_ini[4][4] = board8.disc['white']
    assert board8._board == board8_ini

    print(board10)
    board10_ini = [[board10.disc['blank'] for _ in range(10)] for _ in range(10)]
    board10_ini[5][4] = board10.disc['black']
    board10_ini[4][5] = board10.disc['black']
    board10_ini[4][4] = board10.disc['white']
    board10_ini[5][5] = board10.disc['white']
    assert board10._board == board10_ini

    print(board26)
    board26_ini = [[board26.disc['blank'] for _ in range(26)] for _ in range(26)]
    board26_ini[13][12] = board26.disc['black']
    board26_ini[12][13] = board26.disc['black']
    board26_ini[12][12] = board26.disc['white']
    board26_ini[13][13] = board26.disc['white']
    assert board26._board == board26_ini

    # 石を置く
    assert board4.put_disc('black', 0, 0) == []
    assert board4.put_disc('black', 3, 5) == []
    assert board4.put_disc('black', 1, 0) == [(1, 1)]
    assert board4.put_disc('white', 0, 0) == [(1, 1)]
    assert board4.put_disc('black', 0, 1) == [(1, 1)]
    assert board4.put_disc('white', 2, 0) == [(2, 1), (1, 0)]
    assert board4.put_disc('black', 3, 0) == [(2, 1)]
    assert board4.put_disc('white', 1, 3) == [(1, 2), (1, 1)]
    assert board4.put_disc('black', 0, 3) == [(1, 2)]
    assert board4.put_disc('white', 0, 2) == [(1, 2), (0, 1)]
    assert board4.put_disc('black', 2, 3) == [(1, 3), (2, 2)]
    assert board4.put_disc('white', 3, 2) == [(2, 2), (2, 1)]
    assert board4.put_disc('black', 3, 1) == [(2, 2)]
    assert board4.put_disc('white', 3, 3) == [(2, 2)]

    assert board4.get_bitboard_info() == (4366, 61169)

    # プレイ結果
    print(board4)
    board4_ret = [[board4.disc['blank'] for _ in range(4)] for _ in range(4)]
    board4_ret[0][0] = board4.disc['white']
    board4_ret[0][1] = board4.disc['white']
    board4_ret[0][2] = board4.disc['white']
    board4_ret[0][3] = board4.disc['black']
    board4_ret[1][0] = board4.disc['white']
    board4_ret[1][1] = board4.disc['white']
    board4_ret[1][2] = board4.disc['white']
    board4_ret[1][3] = board4.disc['black']
    board4_ret[2][0] = board4.disc['white']
    board4_ret[2][1] = board4.disc['white']
    board4_ret[2][2] = board4.disc['white']
    board4_ret[2][3] = board4.disc['white']
    board4_ret[3][0] = board4.disc['black']
    board4_ret[3][1] = board4.disc['black']
    board4_ret[3][2] = board4.disc['black']
    board4_ret[3][3] = board4.disc['white']
    assert board4._board == board4_ret
    assert board4.score['black'] == 5
    assert board4.score['white'] == 11

    print(board4.get_board_info())

    # やり直し
    board4 = Board(4)
    board4.put_disc('black', 0, 1)
    print(board4)
    assert board4.score['black'] == 4
    assert board4.score['white'] == 1
    board4.undo()
    print(board4)
    assert board4.score['black'] == 2
    assert board4.score['white'] == 2
    board4.put_disc('white', 0, 2)
    print(board4)
    board4.undo()
    print(board4)

    # ============ #
    # ビットボード #
    # ============ #
    bitboard4 = BitBoard(4)
    bitboard8 = BitBoard(8)
    bitboard10 = BitBoard(10)
    bitboard20 = BitBoard(20)
    bitboard26 = BitBoard(26)

    # 初期位置
    assert bitboard4._black_bitboard == 0x240
    assert bitboard4._white_bitboard == 0x420
    assert bitboard8._black_bitboard == 0x810000000
    assert bitboard8._white_bitboard == 0x1008000000

    # mask
    assert bitboard4._mask.h == 0x6666
    assert bitboard4._mask.v == 0x0FF0
    assert bitboard4._mask.d == 0x0660
    assert bitboard4._mask.u == 0xFFF0
    assert bitboard4._mask.ur == 0x7770
    assert bitboard4._mask.r == 0x7777
    assert bitboard4._mask.br == 0x0777
    assert bitboard4._mask.b == 0x0FFF
    assert bitboard4._mask.bl == 0x0EEE
    assert bitboard4._mask.l == 0xEEEE
    assert bitboard4._mask.ul == 0xEEE0

    assert bitboard8._mask.h == 0x7E7E7E7E7E7E7E7E
    assert bitboard8._mask.v == 0x00FFFFFFFFFFFF00
    assert bitboard8._mask.d == 0x007E7E7E7E7E7E00
    assert bitboard8._mask.u == 0xFFFFFFFFFFFFFF00
    assert bitboard8._mask.ur == 0x7F7F7F7F7F7F7F00
    assert bitboard8._mask.r == 0x7F7F7F7F7F7F7F7F
    assert bitboard8._mask.br == 0x007F7F7F7F7F7F7F
    assert bitboard8._mask.b == 0x00FFFFFFFFFFFFFF
    assert bitboard8._mask.bl == 0x00FEFEFEFEFEFEFE
    assert bitboard8._mask.l == 0xFEFEFEFEFEFEFEFE
    assert bitboard8._mask.ul == 0xFEFEFEFEFEFEFE00

    # get_legal_moves
    bitboard4._black_bitboard = 0x640
    bitboard4._white_bitboard = 0x020
    legal_moves = bitboard4.get_legal_moves('black')
    assert legal_moves == {(3, 2): [(2, 2)], (2, 3): [(2, 2)], (3, 3): [(2, 2)]}
    legal_moves = bitboard4.get_legal_moves('white')
    assert legal_moves == {(0, 0): [(1, 1)], (2, 0): [(2, 1)], (0, 2): [(1, 2)]}

    bitboard4._black_bitboard = 0x040
    bitboard4._white_bitboard = 0x620
    legal_moves = bitboard4.get_legal_moves('black')
    assert legal_moves == {(1, 0): [(1, 1)], (3, 0): [(2, 1)], (3, 2): [(2, 2)]}
    legal_moves = bitboard4.get_legal_moves('white')
    assert legal_moves == {(0, 2): [(1, 2)], (0, 3): [(1, 2)], (1, 3): [(1, 2)]}

    bitboard4._black_bitboard = 0x260
    bitboard4._white_bitboard = 0x400
    legal_moves = bitboard4.get_legal_moves('black')
    assert legal_moves == {(0, 0): [(1, 1)], (1, 0): [(1, 1)], (0, 1): [(1, 1)]}
    legal_moves = bitboard4.get_legal_moves('white')
    assert legal_moves == {(3, 1): [(2, 1)], (1, 3): [(1, 2)], (3, 3): [(2, 2)]}

    bitboard4._black_bitboard = 0x200
    bitboard4._white_bitboard = 0x460
    legal_moves = bitboard4.get_legal_moves('black')
    assert legal_moves == {(0, 1): [(1, 1)], (0, 3): [(1, 2)], (2, 3): [(2, 2)]}
    legal_moves = bitboard4.get_legal_moves('white')
    assert legal_moves == {(2, 0): [(2, 1)], (3, 0): [(2, 1)], (3, 1): [(2, 1)]}

    # put_disc
    bitboard4._black_bitboard = 0x240
    bitboard4._white_bitboard = 0x420

    print('BitBoard')
    print(bitboard4)
    assert len(bitboard4.put_disc('black', 1, 0)) == 1
    assert bitboard4.prev == [{'color': 'black', 'x': 1, 'y': 0, 'flippable_discs': 1024, 'disc_num': 1}]
    assert len(bitboard4.put_disc('white', 0, 0)) == 1
    assert bitboard4.prev == [{'color': 'black', 'x': 1, 'y': 0, 'flippable_discs': 1024, 'disc_num': 1}, {'color': 'white', 'x': 0, 'y': 0, 'flippable_discs': 1024, 'disc_num': 1}]
    assert len(bitboard4.put_disc('black', 0, 1)) == 1
    assert len(bitboard4.put_disc('white', 2, 0)) == 2
    assert len(bitboard4.put_disc('black', 3, 2)) == 1
    assert len(bitboard4.put_disc('white', 3, 3)) == 2
    assert len(bitboard4.put_disc('black', 3, 1)) == 2
    assert len(bitboard4.put_disc('white', 3, 0)) == 2
    assert len(bitboard4.put_disc('black', 2, 3)) == 1
    assert len(bitboard4.put_disc('white', 1, 3)) == 4
    assert len(bitboard4.put_disc('black', 0, 3)) == 1
    print(bitboard4)
    assert len(bitboard4.put_disc('white', 0, 2)) == 2
    print(bitboard4)

    # score
    assert bitboard4.score['black'] == 2
    assert bitboard4.score['white'] == 14

    # undo
    bitboard4.undo()
    assert bitboard4._black_bitboard == 0x0A48
    assert bitboard4._white_bitboard == 0xF537
    print(bitboard4)

    # get_board_info
    assert bitboard4.get_board_info() == [[-1, -1, -1, -1], [1, -1, 1, -1], [0, 1, -1, -1], [1, -1, -1, -1]]

    # score
    assert bitboard4.score['black'] == 4
    assert bitboard4.score['white'] == 11

    # size8
    bitboard8 = BitBoard(8)
    legal_moves = bitboard8.get_legal_moves('black')
    assert legal_moves == {(3, 2): [(3, 3)], (2, 3): [(3, 3)], (5, 4): [(4, 4)], (4, 5): [(4, 4)]}

    # 全般
    bitboard8 = BitBoard(8)
    bitboard8._black_bitboard = 0x0000240000240000
    bitboard8._white_bitboard = 0x007E5A7A5E5A7E00
    legal_moves = bitboard8.get_legal_moves('black')
    assert legal_moves == {(0, 0): [(1, 1)], (2, 0): [(2, 1)], (3, 0): [(4, 1)], (4, 0): [(3, 1)], (5, 0): [(5, 1)], (7, 0): [(6, 1)], (0, 2): [(1, 2)], (7, 2): [(6, 2)], (0, 3): [(1, 4)], (5, 3): [(5, 4)], (7, 3): [(6, 4)], (0, 4): [(1, 3)], (2, 4): [(2, 3)], (7, 4): [(6, 3)], (0, 5): [(1, 5)], (7, 5): [(6, 5)], (0, 7): [(1, 6)], (2, 7): [(2, 6)], (3, 7): [(4, 6)], (4, 7): [(3, 6)], (5, 7): [(5, 6)], (7, 7): [(6, 6)]}

    # 上黒
    bitboard8 = BitBoard(8)
    bitboard8._black_bitboard = 0x00000001000000BF
    bitboard8._white_bitboard = 0x006573787C7E7F00
    legal_moves = bitboard8.get_legal_moves('black')
    assert legal_moves == {(0, 0): [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)], (2, 0): [(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6)], (4, 0): [(5, 1), (6, 2)], (7, 0): [(7, 1), (7, 2)], (0, 1): [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)], (3, 1): [(3, 2), (3, 3), (3, 4), (3, 5), (3, 6)], (0, 2): [(1, 3), (2, 4), (3, 5), (4, 6)], (4, 2): [(4, 3), (4, 4), (4, 5), (4, 6)], (5, 2): [(4, 3), (3, 4), (2, 5), (1, 6)], (0, 3): [(1, 4), (2, 5), (3, 6)], (5, 3): [(5, 4), (5, 5), (5, 6)], (6, 3): [(5, 4), (4, 5), (3, 6)], (0, 4): [(1, 5), (2, 6)], (6, 4): [(5, 5), (6, 5), (4, 6), (6, 6)], (7, 4): [(6, 5), (5, 6)], (0, 5): [(1, 6)], (7, 5): [(6, 6), (7, 6)]}

    # 上白
    bitboard8 = BitBoard(8)
    bitboard8._black_bitboard = 0x00A6CE1E3E7EFE00
    bitboard8._white_bitboard = 0x00000080000000FD
    legal_moves = bitboard8.get_legal_moves('white')
    assert legal_moves == {(0, 0): [(0, 1), (0, 2)], (3, 0): [(2, 1), (1, 2)], (5, 0): [(5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6)], (7, 0): [(6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6)], (4, 1): [(4, 2), (4, 3), (4, 4), (4, 5), (4, 6)], (7, 1): [(6, 2), (5, 3), (4, 4), (3, 5), (2, 6)], (2, 2): [(3, 3), (4, 4), (5, 5), (6, 6)], (3, 2): [(3, 3), (3, 4), (3, 5), (3, 6)], (7, 2): [(6, 3), (5, 4), (4, 5), (3, 6)], (1, 3): [(2, 4), (3, 5), (4, 6)], (2, 3): [(2, 4), (2, 5), (2, 6)], (7, 3): [(6, 4), (5, 5), (4, 6)], (0, 4): [(1, 5), (2, 6)], (1, 4): [(1, 5), (2, 5), (1, 6), (3, 6)], (7, 4): [(6, 5), (5, 6)], (0, 5): [(0, 6), (1, 6)], (7, 5): [(6, 6)]}

    # 左黒
    bitboard8 = BitBoard(8)
    bitboard8._black_bitboard = 0x0100010101010111
    bitboard8._white_bitboard = 0x007E7E3E1E4E2662
    legal_moves = bitboard8.get_legal_moves('black')
    assert legal_moves == {(0, 0): [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)], (1, 0): [(2, 1), (3, 2), (4, 3), (5, 4), (6, 5)], (2, 0): [(3, 1), (4, 2), (5, 3), (6, 4)], (3, 0): [(4, 1), (5, 2), (6, 3)], (4, 0): [(5, 1), (6, 2)], (5, 0): [(6, 1)], (0, 2): [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2)], (1, 3): [(2, 3), (3, 3), (4, 3), (5, 3), (6, 3)], (0, 4): [(1, 5), (2, 6)], (2, 4): [(3, 4), (4, 4), (5, 4), (6, 4)], (2, 5): [(6, 1), (5, 2), (4, 3), (3, 4)], (3, 5): [(4, 5), (5, 5), (6, 5)], (3, 6): [(6, 3), (5, 4), (4, 5)], (4, 6): [(6, 4), (5, 5), (5, 6), (6, 6)], (0, 7): [(1, 7), (2, 7)], (4, 7): [(6, 5), (5, 6)], (5, 7): [(6, 6), (6, 7)]}

    # 下黒
    bitboard8 = BitBoard(8)
    bitboard8._black_bitboard = 0xBF00000001000000
    bitboard8._white_bitboard = 0x007F7E7C78736500
    legal_moves = bitboard8.get_legal_moves('black')
    assert legal_moves == {(0, 2): [(1, 1)], (7, 2): [(6, 1), (7, 1)], (0, 3): [(2, 1), (1, 2)], (6, 3): [(4, 1), (6, 1), (5, 2), (6, 2)], (7, 3): [(5, 1), (6, 2)], (0, 4): [(3, 1), (2, 2), (1, 3)], (5, 4): [(5, 1), (5, 2), (5, 3)], (6, 4): [(3, 1), (4, 2), (5, 3)], (0, 5): [(4, 1), (3, 2), (2, 3), (1, 4)], (4, 5): [(4, 1), (4, 2), (4, 3), (4, 4)], (5, 5): [(1, 1), (2, 2), (3, 3), (4, 4)], (0, 6): [(5, 1), (4, 2), (3, 3), (2, 4), (1, 5)], (3, 6): [(3, 1), (3, 2), (3, 3), (3, 4), (3, 5)], (0, 7): [(6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6)], (2, 7): [(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6)], (4, 7): [(6, 5), (5, 6)], (7, 7): [(7, 5), (7, 6)]}

    # 右黒
    bitboard8 = BitBoard(8)
    bitboard8._black_bitboard = 0x8000808080808088
    bitboard8._white_bitboard = 0x007E7E7C78726446
    legal_moves = bitboard8.get_legal_moves('black')
    assert legal_moves == {(2, 0): [(1, 1)], (3, 0): [(2, 1), (1, 2)], (4, 0): [(3, 1), (2, 2), (1, 3)], (5, 0): [(4, 1), (3, 2), (2, 3), (1, 4)], (6, 0): [(5, 1), (4, 2), (3, 3), (2, 4), (1, 5)], (7, 0): [(6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6)], (7, 2): [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2)], (6, 3): [(1, 3), (2, 3), (3, 3), (4, 3), (5, 3)], (5, 4): [(1, 4), (2, 4), (3, 4), (4, 4)], (7, 4): [(6, 5), (5, 6)], (4, 5): [(1, 5), (2, 5), (3, 5)], (5, 5): [(1, 1), (2, 2), (3, 3), (4, 4)], (3, 6): [(1, 4), (2, 5), (1, 6), (2, 6)], (4, 6): [(1, 3), (2, 4), (3, 5)], (2, 7): [(1, 6), (1, 7)], (3, 7): [(1, 5), (2, 6)], (7, 7): [(5, 7), (6, 7)]}

    # test1
    bitboard8 = BitBoard(8)
    bitboard8._black_bitboard = 0x0000000000081000
    bitboard8._white_bitboard = 0x0000001C1C140000
    legal_moves = bitboard8.get_legal_moves('black')
    assert legal_moves == {(3, 2): [(3, 3), (3, 4), (3, 5)], (4, 2): [(4, 3), (4, 4)], (2, 3): [(3, 4)], (6, 3): [(5, 4)], (2, 5): [(3, 5)], (6, 5): [(5, 5)]}

    # get_bitboard_info
    assert bitboard8.get_bitboard_info() == (0x0000000000081000, 0x0000001C1C140000)