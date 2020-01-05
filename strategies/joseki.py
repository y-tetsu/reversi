#!/usr/bin/env python
"""
定石打ち
"""

import sys
sys.path.append('../')

from strategies.common import CPU_TIME, AbstractStrategy
from strategies.timer import Timer
from strategies.measure import Measure
from strategies.fullreading import AbIF11_B_TPW, MultiNsF11


# ===== 定石リスト =====
JOSEKI = {
    #---------------------------------------------------------------------
    # 1手目
    # □□□□□□□□
    # □□□□□□□□
    # □□□□□□□□
    # □□□●〇□□□
    # □□□〇●◎□□
    # □□□□□□□□
    # □□□□□□□□
    # □□□□□□□□
    ('black', 0x0000000810000000, 0x0000001008000000): (5, 4),
    #---------------------------------------------------------------------
    # 2手目(兎定石)
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□◎□□□ □□□□□□□□ □□□〇□□□□
    # □□□●〇□□□ □□〇〇〇□□□ □□□●〇◎□□ □□□〇〇□□□
    # □□□〇〇〇□□ □□□〇●□□□ □□□〇〇□□□ □□◎〇●□□□
    # □□□◎□□□□ □□□□□□□□ □□□□〇□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    ('white', 0x000000081C000000, 0x0000001000000000): (3, 5),
    ('white', 0x0000003810000000, 0x0000000008000000): (4, 2),
    ('white', 0x0000000818080000, 0x0000001000000000): (5, 3),
    ('white', 0x0000101810000000, 0x0000000008000000): (2, 4),
    #---------------------------------------------------------------------
    # 3手目(兎定石)
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□●□□□ □□□□◎□□□ □□□〇□□□□
    # □□□●〇□□□ □□〇〇●◎□□ □□□●●●□□ □□□〇〇□□□
    # □□◎●〇〇□□ □□□〇●□□□ □□□〇〇□□□ □□●●●□□□
    # □□□●□□□□ □□□□□□□□ □□□□〇□□□ □□□◎□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    ('black', 0x000000080C000000, 0x0000001010100000): (2, 4),
    ('black', 0x0000003010000000, 0x0000080808000000): (5, 3),
    ('black', 0x0000000018080000, 0x0000001C00000000): (4, 2),
    ('black', 0x0000101800000000, 0x0000000038000000): (3, 5),
    #---------------------------------------------------------------------
    # 4手目(兎定石)
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□●□□□ □□□□〇□□□ □□□〇◎□□□
    # □□□●〇◎□□ □□〇〇〇〇□□ □□□●〇●□□ □□□〇〇□□□
    # □□〇〇〇〇□□ □□◎〇●□□□ □□□〇〇□□□ □□●〇●□□□
    # □□□●□□□□ □□□□□□□□ □□□◎〇□□□ □□□〇□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    ('white', 0x000000083C000000, 0x0000001000100000): (5, 3),
    ('white', 0x0000003C10000000, 0x0000080008000000): (2, 4),
    ('white', 0x0000080818080000, 0x0000001400000000): (3, 5),
    ('white', 0x0000101810100000, 0x0000000028000000): (4, 2),
    #---------------------------------------------------------------------
    # 5手目(兎定石)
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□◎□□□ □□□□●□□□ □□□□〇□□□ □□□〇●□□□
    # □□□●●●□□ □□〇●〇〇□□ □□□●〇●□□ □□□●●◎□□
    # □□〇〇●〇□□ □□●●●□□□ □□◎●●□□□ □□●〇●□□□
    # □□□●□□□□ □□□◎□□□□ □□□●〇□□□ □□□〇□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    ('black', 0x0000000034000000, 0x0000001C08100000): (4, 2),
    ('black', 0x0000002C00000000, 0x0000081038000000): (3, 5),
    ('black', 0x0000080800080000, 0x0000001418100000): (2, 4),
    ('black', 0x0000100010100000, 0x0000081828000000): (5, 3),
}
# ===== 定石リスト =====


class Joseki(AbstractStrategy):
    """
    定石通りに打つ(8x8限定)
    """
    def __init__(self, base):
        self.joseki = JOSEKI
        self.base = base

    @Measure.time
    def next_move(self, color, board):
        """
        次の一手
        """
        if board.size == 8:
            bitboard_b, bitboard_w = board.get_bitboard_info()
            key = (color, bitboard_b, bitboard_w)

            # 定石リストに手が含まれる場合
            if key in self.joseki:
                return self.joseki[key]

        return self.base.next_move(color, board)


class AbIF11J_B_TPW(Joseki):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める+定石打ち
    (選択的探索:なし、並べ替え:B、評価関数:TPW, 完全読み開始:残り11手)
    """
    def __init__(self, base=AbIF11_B_TPW()):
        super().__init__(base)


class MultiNsF11J(Joseki):
    """
    MultiNegaScout+定石打ち
    (選択的探索:なし、並べ替え:B、評価関数:TPW, 完全読み開始:残り11手)
    """
    def __init__(self, base=MultiNsF11()):
        super().__init__(base)


if __name__ == '__main__':
    from board import BitBoard

    def rotate_180(bbits, wbits, move): # 180°回転
        bbits_tmp = [['0' for i in range(8)] for j in range(8)]
        wbits_tmp = [['0' for i in range(8)] for j in range(8)]

        check = 1 << 63
        for y in range(8):
            for x in range(8):
                if bbits & check:
                    bbits_tmp[y][x] = '1'
                if wbits & check:
                    wbits_tmp[y][x] = '1'
                check >>= 1

        import numpy as np

        bbits_tmp = np.rot90(np.rot90(np.array(bbits_tmp)))
        wbits_tmp = np.rot90(np.rot90(np.array(wbits_tmp)))
        bbits = int(''.join(bbits_tmp.flatten()), 2)
        wbits = int(''.join(wbits_tmp.flatten()), 2)
        move = 7 - move[0], 7 - move[1]

        return bbits, wbits, move

    def delta_swap(bits, mask, delta):
        x = (bits ^ (bits >> delta)) & mask
        return bits ^ x ^ (x << delta)

    def flip_diag(bbits, wbits, move): # 対角線を軸に反転
        bbits = delta_swap(bbits, 0x00000000F0F0F0F0, 28)
        bbits = delta_swap(bbits, 0x0000CCCC0000CCCC, 14)
        bbits = delta_swap(bbits, 0x00AA00AA00AA00AA,  7)
        wbits = delta_swap(wbits, 0x00000000F0F0F0F0, 28)
        wbits = delta_swap(wbits, 0x0000CCCC0000CCCC, 14)
        wbits = delta_swap(wbits, 0x00AA00AA00AA00AA,  7)
        move = move[1], move[0]
        return bbits, wbits, move

    def rotate_flip(color, b, w, move):
        print(f"    ('{color}', 0x{b:016X}, 0x{w:016X}): {move},")
        b2, w2, move2 = rotate_180(b, w, move)
        print(f"    ('{color}', 0x{b2:016X}, 0x{w2:016X}): {move2},")
        b3, w3, move3 = flip_diag(b, w, move)
        print(f"    ('{color}', 0x{b3:016X}, 0x{w3:016X}): {move3},")
        b4, w4, move4 = flip_diag(b2, w2, move2)
        print(f"    ('{color}', 0x{b4:016X}, 0x{w4:016X}): {move4},")


    print('--- Test For AbIF11J_B_TPW Strategy ---')
    joseki = AbIF11J_B_TPW()

    bitboard8 = BitBoard()
    print(bitboard8)

    # 1手目
    move = joseki.next_move('black', bitboard8)
    print(move)
    bitboard8.put_stone('black', *move)
    print(bitboard8)

    # 2手目
    move = joseki.next_move('white', bitboard8)
    print(move)
    bitboard8.put_stone('white', *move)
    print(bitboard8)

    # 3手目
    move = joseki.next_move('black', bitboard8)
    print(move)
    bitboard8.put_stone('black', *move)
    print(bitboard8)

    # 4手目
    move = joseki.next_move('white', bitboard8)
    print(move)
    bitboard8.put_stone('white', *move)
    print(bitboard8)

    # 5手目
    move = joseki.next_move('black', bitboard8)
    print(move)
    bitboard8.put_stone('black', *move)
    print(bitboard8)

    #-----------------------------------#
    #color, move = 'black', (4, 2)
    #b, w =  bitboard8.get_bitboard_info()
    #rotate_flip(color, b, w, move)
    #-----------------------------------#
