"""Board
"""

import abc
from collections import namedtuple

from reversi.color import C as c
from reversi.disc import D as d
import reversi.BitBoardMethods as BitBoardMethods


MIN_BOARD_SIZE = 4
MAX_BOARD_SIZE = 26


class AbstractBoard(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_legal_moves(self, color):
        pass

    @abc.abstractmethod
    def get_legal_moves_bits(self, color):
        pass

    @abc.abstractmethod
    def get_flippable_discs(self, color, x, y):
        pass

    @abc.abstractmethod
    def put_disc(self, color, x, y):
        pass

    @abc.abstractmethod
    def update_score(self):
        pass

    @abc.abstractmethod
    def get_board_info(self):
        pass

    @abc.abstractmethod
    def get_bitboard_info(self):
        pass

    @abc.abstractmethod
    def get_bit_count(self, bits):
        pass

    @abc.abstractmethod
    def undo(self):
        pass


class BoardSizeError(Exception):
    """BoardSizeError
    """
    pass


class Board(AbstractBoard):
    """Board
    """
    def __init__(self, size=8):
        if not(MIN_BOARD_SIZE <= size <= MAX_BOARD_SIZE and size % 2 == 0):  # 意図しないサイズの場合エラー
            raise BoardSizeError(str(size) + ' is invalid size!')

        self.size = size                                 # ボードサイズ
        (self._black_score, self._white_score) = (2, 2)  # スコア
        self.prev = []                                   # 前回の手

        # 盤面
        self._board = [[d[c.blank] for _ in range(size)] for _ in range(size)]  # 一旦ブランクで埋める
        center = size // 2
        init_discs = [
            (center,   center-1, c.black),
            (center-1, center,   c.black),
            (center-1, center-1, c.white),
            (center,   center,   c.white),
        ]
        for x, y, color in init_discs:  # 中央の4石を置く
            self._board[y][x] = d[color]

    def __str__(self):
        header = '   ' + ' '.join([chr(97 + i) for i in range(self.size)]) + '\n'
        body = ''
        for num, row in enumerate(self._board, 1):
            body += f'{num:2d}' + ''.join([value for value in row]) + '\n'

        return header + body

    def get_legal_moves(self, color):
        """get_legal_moves

        Args:
            color : player's color

        Returns:
            legal_moves list
        """
        legal_moves = []
        for y in range(self.size):
            for x in range(self.size):
                flippable_discs = self.get_flippable_discs(color, x, y)
                if flippable_discs:
                    legal_moves += [(x, y)]

        return legal_moves

    def get_legal_moves_bits(self, color):
        """get_legal_moves_bits

        Args:
            color : player's color

        Returns:
            legal_moves bits
        """
        size = self.size
        mask = 1 << ((size**2)-1)
        legal_moves_bits = 0
        for x, y in self.get_legal_moves(color):
            bits = mask >> (y*size+x)
            legal_moves_bits |= bits

        return legal_moves_bits

    def get_flippable_discs(self, color, x, y):
        """get_flippable_discs

               指定座標のひっくり返せる石の場所をすべて返す
        """
        directions = [
            (-1,  1), (0,  1), (1,  1),
            (-1,  0),          (1,  0),
            (-1, -1), (0, -1), (1, -1)
        ]
        ret = []

        # 指定座標が範囲内 かつ 石が置いていない
        if self._in_range(x, y) and self._board[y][x] == d[c.blank]:
            # 8方向をチェック
            for direction in directions:
                tmp = self._get_flippable_discs_in_direction(color, x, y, direction)

                if tmp:
                    ret += tmp

        return ret

    def _get_flippable_discs_in_direction(self, color, x, y, direction):
        """_get_flippable_discs_in_direction

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
                if next_value != d[c.blank]:
                    # 置いた石と同じ色が見つかった場合
                    if next_value == d[color]:
                        return ret

                    ret += [(next_x, next_y)]
                else:
                    break
            else:
                break

        return []

    def _in_range(self, x, y):
        """_in_range

               座標がボードの範囲内かどうかを返す
        """
        if 0 <= x < self.size and 0 <= y < self.size:
            return True

        return False

    def put_disc(self, color, x, y):
        """put_disc

               指定座標に石を置いて返せる場所をひっくり返し、取れた石の座標を返す
        """
        if not self._in_range(x, y):
            return 0

        flippable_discs = self.get_flippable_discs(color, x, y)

        # 指定座標に石を置く
        self._board[y][x] = d[color]

        # ひっくり返せる場所に石を置く
        for tmp_x, tmp_y, in flippable_discs:
            self._board[tmp_y][tmp_x] = d[color]

        self.update_score()

        # 打った手の記録
        self.prev += [{'color': color, 'x': x, 'y': y, 'flippable_discs': flippable_discs}]

        # 返した石のビット
        ret = 0
        size = self.size
        mask = 1 << (size*size-1)
        for y in range(self.size):
            for x in range(self.size):
                if (x, y) in flippable_discs:
                    ret |= mask
                mask >>= 1

        return ret

    def update_score(self):
        """update_score
        """
        self._black_score = sum([row.count(d[c.black]) for row in self._board])
        self._white_score = sum([row.count(d[c.white]) for row in self._board])

    def get_board_info(self):
        """get_board_info
        """
        board_info = []
        for row in self._board:
            tmp = []

            for col in row:
                if col == d[c.black]:
                    tmp += [1]
                elif col == d[c.white]:
                    tmp += [-1]
                elif col == d[c.blank]:
                    tmp += [0]

            board_info += [tmp]

        return board_info

    def get_bit_count(self, bits):
        """get_bit_count
        """
        count = 0
        size = self.size
        mask = 1 << ((size**2)-1)
        for _ in range(size**2):
            if bits & mask:
                count += 1
            mask >>= 1

        return count

    def get_bitboard_info(self):
        """get_bitboard_info
        """
        size = self.size
        black_bitboard, white_bitboard = 0, 0
        put = 1 << size * size - 1
        for y in range(self.size):
            for x in range(self.size):
                if self._board[y][x] == d[c.black]:
                    black_bitboard |= put
                if self._board[y][x] == d[c.white]:
                    white_bitboard |= put
                put >>= 1

        return black_bitboard, white_bitboard

    def undo(self):
        """undo
        """
        prev = self.prev.pop()
        if prev:
            color = prev['color']
            prev_color = c.white if color == c.black else c.black
            x = prev['x']
            y = prev['y']
            flippable_discs = prev['flippable_discs']
            self._board[y][x] = d[c.blank]

            for prev_x, prev_y in flippable_discs:
                self._board[prev_y][prev_x] = d[prev_color]

            self.update_score()


class BitBoard(AbstractBoard):
    """BitBoard
    """
    def __init__(self, size=8):
        if not(MIN_BOARD_SIZE <= size <= MAX_BOARD_SIZE and size % 2 == 0):
            raise BoardSizeError(str(size) + ' is invalid size!')

        # ボードサイズの初期設定
        self.size = size

        # スコアの初期設定
        self._black_score = 2
        self._white_score = 2

        # 前回の手
        self.prev = []
        self._flippable_discs_num = 0

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

    def __str__(self):
        size = self.size
        header = '   ' + ' '.join([chr(97 + i) for i in range(size)]) + '\n'
        board = [[d[c.blank] for _ in range(size)] for _ in range(size)]
        mask = 1 << (size * size - 1)
        for y in range(size):
            for x in range(size):
                if self._black_bitboard & mask:
                    board[y][x] = d[c.black]
                elif self._white_bitboard & mask:
                    board[y][x] = d[c.white]
                mask >>= 1

        body = ''
        for num, row in enumerate(board, 1):
            body += f'{num:2d}' + ''.join([value for value in row]) + '\n'

        return header + body

    def get_legal_moves(self, color):
        """get_legal_moves

        Args:
            color : player's color

        Returns:
            legal_moves list
        """
        return BitBoardMethods.get_legal_moves(color, self.size, self._black_bitboard, self._white_bitboard, self._mask)

    def get_legal_moves_bits(self, color):
        """get_legal_moves_bits

        Args:
            color : player's color

        Returns:
            legal_moves bits
        """
        return BitBoardMethods.get_legal_moves_bits(color, self.size, self._black_bitboard, self._white_bitboard, self._mask)

    def get_flippable_discs(self, color, x, y):
        """get_flippable_discs

               指定座標のひっくり返せる石の場所をすべて返す
        """
        return BitBoardMethods.get_flippable_discs(color, self.size, self._black_bitboard, self._white_bitboard, x, y, self._mask)

    def put_disc(self, color, x, y):
        """put_disc

               指定座標に石を置いて返せる場所をひっくり返し、取れた石の座標を返す
        """
        return BitBoardMethods.put_disc(self, color, x, y)

    def update_score(self):
        """update_score
        """
        self._black_score, self._white_score = 0, 0
        size = self.size
        mask = 1 << (size * size - 1)
        for y in range(size):
            for x in range(size):
                if self._black_bitboard & mask:
                    self._black_score += 1
                elif self._white_bitboard & mask:
                    self._white_score += 1
                mask >>= 1

    def get_board_info(self):
        """get_board_info
        """
        return BitBoardMethods.get_board_info(self.size, self._black_bitboard, self._white_bitboard)

    def get_bit_count(self, bits):
        """get_git_count
        """
        return BitBoardMethods.get_bit_count(self.size, bits)

    def get_bitboard_info(self):
        """get_bitboard_info
        """
        return self._black_bitboard, self._white_bitboard

    def undo(self):
        """undo
        """
        BitBoardMethods.undo(self)
