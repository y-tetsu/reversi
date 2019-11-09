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

        # 置ける場所のキャッシュ
        self._possibles_cache = {}

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
        # キャッシュが存在する場合
        if color in self._possibles_cache:
            return self._possibles_cache[color]

        self._possibles_cache.clear()
        possibles = {}

        for y in range(self.size):
            for x in range(self.size):
                reversibles = self._get_reversibles(color, x, y)

                if reversibles:
                    possibles[(x, y)] = reversibles

        self._possibles_cache[color] = possibles

        return possibles

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

            self._update_stone_num()


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
        self.stone, self.score = {}, {}
        factory = StoneFactory()

        for color in ('black', 'white', 'blank'):
            self.stone[color] = factory.create(color)
            if color != 'blank':
                self.score[color] = 2

        # 前回の手
        self.prev = {}

        # ビットボードの初期配置
        center = size // 2
        self._black_bitboard = 1 << ((size*size-1)-(size*(center-1)+center))
        self._black_bitboard |= 1 << ((size*size-1)-(size*center+(center-1)))
        self._white_bitboard = 1 << ((size*size-1)-(size*(center-1)+(center-1)))
        self._white_bitboard |= 1 << ((size*size-1)-(size*center+center))

        # 置ける場所の検出用
        self._h_mask = int(''.join((['0'] + ['1'] * (size-2) + ['0']) * size), 2)                                      # 水平方向のマスク値
        self._v_mask = int(''.join(['0'] * size + ['1'] * size * (size-2) + ['0'] * size), 2)                          # 垂直方向のマスク値
        self._d_mask = int(''.join(['0'] * size + (['0'] + (['1'] * (size-2)) + ['0']) * (size-2) + ['0'] * size), 2)  # 斜め方向のマスク値

        # ひっくり返せる場所の検出用
        self._u_mask = int(''.join(['1'] * size * (size-1) + ['0'] * size), 2)                 # 上方向のマスク値
        self._ur_mask = int(''.join((['0'] + ['1'] * (size-1)) * (size-1) + ['0'] * size), 2)  # 右上方向のマスク値
        self._r_mask = int(''.join((['0'] + ['1'] * (size-1)) * size), 2)                      # 右方向のマスク値
        self._br_mask = int(''.join(['0'] * size + (['0'] + ['1'] * (size-1)) * (size-1)), 2)  # 右下方向のマスク値
        self._b_mask = int(''.join(['0'] * size + ['1'] * size * (size-1)), 2)                 # 下方向のマスク値
        self._bl_mask = int(''.join(['0'] * size + (['1'] * (size-1) + ['0']) * (size-1)), 2)  # 左下方向のマスク値
        self._l_mask = int(''.join((['1'] * (size-1) + ['0']) * size), 2)                      # 左方向のマスク値
        self._ul_mask = int(''.join((['1'] * (size-1) + ['0']) * (size-1) + ['0'] * size), 2)  # 左上方向のマスク値

        # 置ける場所のキャッシュ
        self._possibles_cache = {}

    def __str__(self):
        size = self.size

        # 列の見出し
        header = '   ' + ' '.join([chr(97 + i) for i in range(size)]) + '\n'

        # 行の見出し+盤面
        board = [[self.stone['blank'] for _ in range(size)] for _ in range(size)]

        mask = 1 << (size * size - 1)
        for y in range(size):
            for x in range(size):
                if self._black_bitboard & mask:
                    board[y][x] = self.stone['black']
                elif self._white_bitboard & mask:
                    board[y][x] = self.stone['white']
                mask >>= 1

        body = ''
        for num, row in enumerate(board, 1):
            body += f'{num:2d}' + ''.join([value for value in row]) + '\n'

        return header + body

    def get_possibles(self, color):
        """
        石が置ける場所をすべて返す
        """
        # キャッシュが存在する場合
        if color in self._possibles_cache:
            return self._possibles_cache[color]

        self._possibles_cache.clear()
        ret = {}

        # 前準備
        size = self.size
        b, w = self._black_bitboard, self._white_bitboard
        player, opponent = (b, w) if color == 'black' else (w, b)  # プレイヤーと相手を決定
        possibles = 0                                              # 石が置ける場所
        horizontal = opponent & self._h_mask                       # 水平方向のチェック値
        vertical = opponent & self._v_mask                         # 垂直方向のチェック値
        diagonal = opponent & self._d_mask                         # 斜め方向のチェック値
        blank = ~(player | opponent)                               # 空きマス位置

        # 置ける場所を探す
        possibles |= self._get_possibles_lshift(horizontal, player, blank, 1)     # 左方向
        possibles |= self._get_possibles_rshift(horizontal, player, blank, 1)     # 右方向
        possibles |= self._get_possibles_lshift(vertical, player, blank, size)    # 上方向
        possibles |= self._get_possibles_rshift(vertical, player, blank, size)    # 下方向
        possibles |= self._get_possibles_lshift(diagonal, player, blank, size+1)  # 左斜め上方向
        possibles |= self._get_possibles_lshift(diagonal, player, blank, size-1)  # 右斜め上方向
        possibles |= self._get_possibles_rshift(diagonal, player, blank, size-1)  # 左斜め下方向
        possibles |= self._get_possibles_rshift(diagonal, player, blank, size+1)  # 右斜め下方向

        # 石が置ける場所を格納
        mask = 1 << (size * size - 1)
        for y in range(size):
            for x in range(size):
                # 石が置ける場合
                if possibles & mask:
                    ret[(x, y)] = self._get_reversibles(player, opponent, x, y)
                mask >>= 1

        self._possibles_cache[color] = ret

        return ret

    def _get_reversibles(self, player, opponent, x, y):
        """
        指定座標のひっくり返せる石の場所をすべて返す
        """
        ret = []
        reversibles = 0

        # 石を置く場所
        size = self.size
        put = 1 << ((size*size-1)-(y*size+x))

        # 8方向を順番にチェック
        for direction in ('U', 'UR', 'R', 'BR', 'B', 'BL', 'L', 'UL'):
            tmp = 0
            mask = self._get_next_put(put, direction)

            # ボードの範囲内 かつ 相手の石が存在する 限り位置を記憶
            while mask and mask & opponent:
                tmp |= mask
                mask = self._get_next_put(mask, direction)

            # 自分の石で囲まれている場合は結果を格納する
            if mask & player:
                reversibles |= tmp

        # 配列に変換
        size = self.size
        mask = 1 << (size * size - 1)
        for y in range(size):
            for x in range(size):
                if reversibles & mask:
                    ret += [(x, y)]
                mask >>= 1

        return ret

    def _get_next_put(self, put, direction):
        """
        指定位置から指定方向に1マス分移動した場所を返す
        """
        if direction == 'U':     # 上
            return (put << self.size) & self._u_mask
        elif direction == 'UR':  # 右上
            return (put << (self.size-1)) & self._ur_mask
        elif direction == 'R':   # 右
            return (put >> 1) & self._r_mask
        elif direction == 'BR':  # 右下
            return (put >> (self.size+1)) & self._br_mask
        elif direction == 'B':   # 下
            return (put >> self.size) & self._b_mask
        elif direction == 'BL':  # 左下
            return (put >> (self.size-1)) & self._bl_mask
        elif direction == 'L':   # 左
            return (put << 1) & self._l_mask
        elif direction == 'UL':  # 左上
            return (put << (self.size+1)) & self._ul_mask
        else:
            return 0

    def _get_possibles_lshift(self, mask, player, blank, shift_size):
        """
        左シフトで石が置ける場所を取得
        """
        tmp = mask & (player << shift_size)
        for _ in range(self.size-3):
            tmp |= mask & (tmp << shift_size)
        return blank & (tmp << shift_size)

    def _get_possibles_rshift(self, mask, player, blank, shift_size):
        """
        右シフトで石が置ける場所を取得
        """
        tmp = mask & (player >> shift_size)
        for _ in range(self.size-3):
            tmp |= mask & (tmp >> shift_size)
        return blank & (tmp >> shift_size)

    def put_stone(self, color, x, y):
        """
        指定座標に石を置いて返せる場所をひっくり返し、取れた石の座標を返す
        """
        possibles = self.get_possibles(color)

        if (x, y) in possibles:
            # 配置位置を整数に変換
            size = self.size
            put = 1 << ((size*size-1)-(y*size+x))

            # 反転位置を整数に変換
            reversibles_list = possibles[(x, y)]
            tmp = ['0'] * size * size
            for tmp_x, tmp_y in reversibles_list:
                tmp[tmp_y * size + tmp_x] = '1'
            reversibles = int(''.join(tmp), 2)

            # 自分の石を置いて相手の石をひっくり返す
            if color == 'black':
                self._black_bitboard ^= put | reversibles
                self._white_bitboard ^= reversibles
                self.score['black'] += 1 + len(reversibles_list)
                self.score['white'] -= len(reversibles_list)
            else:
                self._white_bitboard ^= put | reversibles
                self._black_bitboard ^= reversibles
                self.score['black'] -= len(reversibles_list)
                self.score['white'] += 1 + len(reversibles_list)

            # 打った手の記録
            self.prev = {'color': color, 'x': x, 'y': y, 'reversibles': reversibles, 'stone_num': len(reversibles_list)}

            return reversibles_list

        return []

    def get_board_info(self):
        """
        ボードの情報を返す
        """
        board_info = []
        size = self.size
        mask = 1 << (size * size - 1)
        for y in range(size):
            tmp = []
            for x in range(size):
                if self._black_bitboard & mask:
                    tmp.append(1)
                elif self._white_bitboard & mask:
                    tmp.append(-1)
                else:
                    tmp.append(0)
                mask >>= 1
            board_info.append(tmp)

        return board_info

    def undo(self):
        """
        やり直し
        """
        if self.prev:
            size, prev = self.size, self.prev
            reversibles, stone_num = self.prev['reversibles'], self.prev['stone_num']

            put = 1 << ((size*size-1)-(self.prev['y']*size+self.prev['x']))

            if prev['color'] == 'black':
                self._black_bitboard ^= put | reversibles
                self._white_bitboard ^= reversibles
                self.score['black'] -= 1 + stone_num
                self.score['white'] += stone_num
            else:
                self._white_bitboard ^= put | reversibles
                self._black_bitboard ^= reversibles
                self.score['black'] += stone_num
                self.score['white'] -= 1 + stone_num


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
    assert board4.score['black'] == 4
    assert board4.score['white'] == 1
    board4.undo()
    print(board4)
    assert board4.score['black'] == 2
    assert board4.score['white'] == 2
    board4.put_stone('white', 0, 2)
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
    assert bitboard4._h_mask == 0x6666
    assert bitboard4._v_mask == 0x0FF0
    assert bitboard4._d_mask == 0x0660
    assert bitboard4._u_mask == 0xFFF0
    assert bitboard4._ur_mask == 0x7770
    assert bitboard4._r_mask == 0x7777
    assert bitboard4._br_mask == 0x0777
    assert bitboard4._b_mask == 0x0FFF
    assert bitboard4._bl_mask == 0x0EEE
    assert bitboard4._l_mask == 0xEEEE
    assert bitboard4._ul_mask == 0xEEE0

    assert bitboard8._h_mask == 0x7E7E7E7E7E7E7E7E
    assert bitboard8._v_mask == 0x00FFFFFFFFFFFF00
    assert bitboard8._d_mask == 0x007E7E7E7E7E7E00
    assert bitboard8._u_mask == 0xFFFFFFFFFFFFFF00
    assert bitboard8._ur_mask == 0x7F7F7F7F7F7F7F00
    assert bitboard8._r_mask == 0x7F7F7F7F7F7F7F7F
    assert bitboard8._br_mask == 0x007F7F7F7F7F7F7F
    assert bitboard8._b_mask == 0x00FFFFFFFFFFFFFF
    assert bitboard8._bl_mask == 0x00FEFEFEFEFEFEFE
    assert bitboard8._l_mask == 0xFEFEFEFEFEFEFEFE
    assert bitboard8._ul_mask == 0xFEFEFEFEFEFEFE00

    # get_possibles
    bitboard4._black_bitboard = 0x640
    bitboard4._white_bitboard = 0x020
    possibles = bitboard4.get_possibles('black')
    assert possibles == {(3, 2): [(2, 2)], (2, 3): [(2, 2)], (3, 3): [(2, 2)]}
    possibles = bitboard4.get_possibles('white')
    assert possibles == {(0, 0): [(1, 1)], (2, 0): [(2, 1)], (0, 2): [(1, 2)]}

    bitboard4._black_bitboard = 0x040
    bitboard4._white_bitboard = 0x620
    possibles = bitboard4.get_possibles('black')
    assert possibles == {(1, 0): [(1, 1)], (3, 0): [(2, 1)], (3, 2): [(2, 2)]}
    possibles = bitboard4.get_possibles('white')
    assert possibles == {(0, 2): [(1, 2)], (0, 3): [(1, 2)], (1, 3): [(1, 2)]}

    bitboard4._black_bitboard = 0x260
    bitboard4._white_bitboard = 0x400
    possibles = bitboard4.get_possibles('black')
    assert possibles == {(0, 0): [(1, 1)], (1, 0): [(1, 1)], (0, 1): [(1, 1)]}
    possibles = bitboard4.get_possibles('white')
    assert possibles == {(3, 1): [(2, 1)], (1, 3): [(1, 2)], (3, 3): [(2, 2)]}

    bitboard4._black_bitboard = 0x200
    bitboard4._white_bitboard = 0x460
    possibles = bitboard4.get_possibles('black')
    assert possibles == {(0, 1): [(1, 1)], (0, 3): [(1, 2)], (2, 3): [(2, 2)]}
    possibles = bitboard4.get_possibles('white')
    assert possibles == {(2, 0): [(2, 1)], (3, 0): [(2, 1)], (3, 1): [(2, 1)]}

    # put_stone
    bitboard4._black_bitboard = 0x240
    bitboard4._white_bitboard = 0x420

    print('BitBoard')
    print(bitboard4)
    assert len(bitboard4.put_stone('black', 1, 0)) == 1
    assert bitboard4.prev == {'color': 'black', 'x': 1, 'y': 0, 'reversibles': 1024, 'stone_num': 1}
    assert len(bitboard4.put_stone('white', 0, 0)) == 1
    assert bitboard4.prev == {'color': 'white', 'x': 0, 'y': 0, 'reversibles': 1024, 'stone_num': 1}
    assert len(bitboard4.put_stone('black', 0, 1)) == 1
    assert len(bitboard4.put_stone('white', 2, 0)) == 2
    assert len(bitboard4.put_stone('black', 3, 2)) == 1
    assert len(bitboard4.put_stone('white', 3, 3)) == 2
    assert len(bitboard4.put_stone('black', 3, 1)) == 2
    assert len(bitboard4.put_stone('white', 3, 0)) == 2
    assert len(bitboard4.put_stone('black', 2, 3)) == 1
    assert len(bitboard4.put_stone('white', 1, 3)) == 4
    assert len(bitboard4.put_stone('black', 0, 3)) == 1
    print(bitboard4)
    assert len(bitboard4.put_stone('white', 0, 2)) == 2
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
