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
        if self._is_invalid_size(size):
            raise BoardSizeError(str(size) + ' is invalid size!')

        self.size = size                                 # ボードサイズ
        (self._black_score, self._white_score) = (2, 2)  # スコア
        self.prev = []                                   # 前回の手

        # 盤面
        self._board = [[d.blank for _ in range(size)] for _ in range(size)]  # 一旦ブランクで埋める
        center = size // 2
        init_discs = [
            (center,   center-1, d.black),
            (center-1, center,   d.black),
            (center-1, center-1, d.white),
            (center,   center,   d.white),
        ]
        for x, y, disc in init_discs:  # 中央の4石を置く
            self._board[y][x] = disc

    def _is_invalid_size(self, size):
        """_is_invalid_size

               無効なボードサイズの場合Trueを返す
        """
        return not(MIN_BOARD_SIZE <= size <= MAX_BOARD_SIZE and size % 2 == 0)

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
                if self.get_flippable_discs(color, x, y):
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
        # 指定座標が範囲内 かつ 石が置かれていない(ブランクである)
        if self._in_range(x, y) and self._is_blank(x, y):
            # 8方向をチェック
            for direction in directions:
                discs = self._get_flippable_discs_in_direction(color, x, y, direction)
                if discs:
                    ret += discs

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
            # 座標が範囲内 かつ 石が置かれている(ブランクではない)
            if self._in_range(next_x, next_y) and not self._is_blank(next_x, next_y):
                # 置いた石と同じ色が見つかった場合
                if self._is_same_color(next_x, next_y, color):
                    return ret

                ret += [(next_x, next_y)]
            else:
                break

        return []

    def _in_range(self, x, y):
        """_in_range

               座標がボードの範囲内の場合True
        """
        return 0 <= x < self.size and 0 <= y < self.size

    def _is_blank(self, x, y):
        """_is_blank

               座標上に石が置かれていない(ブランク)場合True
        """
        return self._board[y][x] == d.blank

    def _is_black(self, x, y):
        """_is_black

               座標上に黒が置かれている場合True
        """
        return self._board[y][x] == d.black

    def _is_white(self, x, y):
        """_is_white

               座標上に白が置かれている場合True
        """
        return self._board[y][x] == d.white

    def _is_same_color(self, x, y, color):
        """_is_same_color

               座標上に同じ色の石が置かれている場合True
        """
        return self._board[y][x] == d[color]

    def put_disc(self, color, x, y):
        """put_disc

               指定座標に石を置いて返せる場所をひっくり返し、取れた石のビット位置を返す
        """
        if not self._in_range(x, y):
            return 0

        flippable_discs = self.get_flippable_discs(color, x, y)  # ひっくり返せる場所を取得
        self._board[y][x] = d[color]                             # 指定座標に石を置く

        # ひっくり返せる場所に石を置く
        for tmp_x, tmp_y, in flippable_discs:
            self._board[tmp_y][tmp_x] = d[color]

        self.update_score()                                                                  # スコア更新
        self.prev += [{'color': color, 'x': x, 'y': y, 'flippable_discs': flippable_discs}]  # 打った手の記録

        return self._get_bit_pos(flippable_discs)

    def update_score(self):
        """update_score
        """
        self._black_score = sum([row.count(d.black) for row in self._board])
        self._white_score = sum([row.count(d.white) for row in self._board])

    def _get_bit_pos(self, discs):
        """_get_bit_pos

               discs配列の石が置いてあるビット位置を返す
        """
        ret = 0
        size = self.size
        mask = 1 << (size*size-1)
        for y in range(self.size):
            for x in range(self.size):
                if (x, y) in discs:
                    ret |= mask
                mask >>= 1

        return ret

    def get_board_info(self):
        """get_board_info
        """
        board_info = []
        for row in self._board:
            tmp = []
            for col in row:
                if d.is_black(col):
                    tmp += [1]
                elif d.is_white(col):
                    tmp += [-1]
                else:
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
                if self._is_black(x, y):
                    black_bitboard |= put
                elif self._is_white(x, y):
                    white_bitboard |= put
                put >>= 1

        return black_bitboard, white_bitboard

    def undo(self):
        """undo
        """
        prev = self.prev.pop()
        self._board[prev['y']][prev['x']] = d.blank     # 置いた石を取り除く
        for prev_x, prev_y in prev['flippable_discs']:  # ひっくり返された石を反転させる
            self._board[prev_y][prev_x] = d[c.next_color(prev['color'])]
        self.update_score()


class BitBoard(AbstractBoard):
    """BitBoard
    """
    def __init__(self, size=8):
        if self._is_invalid_size(size):
            raise BoardSizeError(str(size) + ' is invalid size!')

        self.size = size                                 # ボードサイズ
        (self._black_score, self._white_score) = (2, 2)  # スコア
        self.prev = []                                   # 前回の手

        # ビットボードの初期配置
        center = size // 2
        self._black_bitboard = 1 << ((size*size-1)-(size*(center-1)+center))
        self._black_bitboard |= 1 << ((size*size-1)-(size*center+(center-1)))
        self._white_bitboard = 1 << ((size*size-1)-(size*(center-1)+(center-1)))
        self._white_bitboard |= 1 << ((size*size-1)-(size*center+center))

        # 置ける場所の検出用マスク
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

    def _is_invalid_size(self, size):
        """_is_invalid_size

               無効なボードサイズの場合
        """
        return not(MIN_BOARD_SIZE <= size <= MAX_BOARD_SIZE and size % 2 == 0)

    def __str__(self):
        size = self.size
        header = '   ' + ' '.join([chr(97 + i) for i in range(size)]) + '\n'
        board = [[d.blank for _ in range(size)] for _ in range(size)]
        mask = 1 << (size * size - 1)
        for y in range(size):
            for x in range(size):
                if self._black_bitboard & mask:
                    board[y][x] = d.black
                elif self._white_bitboard & mask:
                    board[y][x] = d.white
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
