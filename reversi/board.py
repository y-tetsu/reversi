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

        return black_bitboard, white_bitboard


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
        return BitBoardMethods.put_disc(self, color, x, y)

    def get_board_info(self):
        """
        ボードの情報を返す
        """
        return BitBoardMethods.get_board_info(self.size, self._black_bitboard, self._white_bitboard)

    def undo(self):
        """
        やり直し
        """
        BitBoardMethods.undo(self)

    def get_bitboard_info(self):
        """
        ビットボードの情報を返す
        """
        return self._black_bitboard, self._white_bitboard
