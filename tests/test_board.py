#!/usr/bin/env python
"""
ボードのテスト
"""

import unittest
from reversi.board import BoardSizeError, Board, BitBoard


class TestBoard(unittest.TestCase):
    """
    通常のボード
    """
    def test_board_size_2(self):
        err = False

        try:
            board2 = Board(2)
        except BoardSizeError as e:
            err = True

        self.assertTrue(err)

    def test_board_size_3(self):
        err = False

        try:
            board2 = Board(3)
        except BoardSizeError as e:
            err = True

        self.assertTrue(err)

#if __name__ == '__main__':
#    # ========== #
#    # 通常ボード #
#    # ========== #
#    # サイズ異常
#    invalid2 = False
#    try:
#        board2 = Board(2)
#    except BoardSizeError as e:
#        print(e)
#        invalid2 = True
#
#    assert invalid2
#
#    invalid3 = False
#    try:
#        board3 = Board(3)
#    except BoardSizeError as e:
#        print(e)
#        invalid3 = True
#
#    assert invalid3
#
#    invalid28 = False
#    try:
#        board28 = Board(28)
#    except BoardSizeError as e:
#        print(e)
#        invalid28 = True
#
#    assert invalid28
#
#    # 初期値
#    board4 = Board(4)
#    board6 = Board(6)
#    board8 = Board()
#    board10 = Board(10)
#    board26 = Board(26)
#
#    print(board4)
#    board4_ini = [[board4.disc['blank'] for _ in range(4)] for _ in range(4)]
#    board4_ini[2][1] = board4.disc['black']
#    board4_ini[1][2] = board4.disc['black']
#    board4_ini[1][1] = board4.disc['white']
#    board4_ini[2][2] = board4.disc['white']
#    assert board4._board == board4_ini
#
#    print(board6)
#    board6_ini = [[board6.disc['blank'] for _ in range(6)] for _ in range(6)]
#    board6_ini[3][2] = board6.disc['black']
#    board6_ini[2][3] = board6.disc['black']
#    board6_ini[2][2] = board6.disc['white']
#    board6_ini[3][3] = board6.disc['white']
#    assert board6._board == board6_ini
#
#    print(board8)
#    board8_ini = [[board8.disc['blank'] for _ in range(8)] for _ in range(8)]
#    board8_ini[4][3] = board8.disc['black']
#    board8_ini[3][4] = board8.disc['black']
#    board8_ini[3][3] = board8.disc['white']
#    board8_ini[4][4] = board8.disc['white']
#    assert board8._board == board8_ini
#
#    print(board10)
#    board10_ini = [[board10.disc['blank'] for _ in range(10)] for _ in range(10)]
#    board10_ini[5][4] = board10.disc['black']
#    board10_ini[4][5] = board10.disc['black']
#    board10_ini[4][4] = board10.disc['white']
#    board10_ini[5][5] = board10.disc['white']
#    assert board10._board == board10_ini
#
#    print(board26)
#    board26_ini = [[board26.disc['blank'] for _ in range(26)] for _ in range(26)]
#    board26_ini[13][12] = board26.disc['black']
#    board26_ini[12][13] = board26.disc['black']
#    board26_ini[12][12] = board26.disc['white']
#    board26_ini[13][13] = board26.disc['white']
#    assert board26._board == board26_ini
#
#    # 石を置く
#    assert board4.put_disc('black', 0, 0) == []
#    assert board4.put_disc('black', 3, 5) == []
#    assert board4.put_disc('black', 1, 0) == [(1, 1)]
#    assert board4.put_disc('white', 0, 0) == [(1, 1)]
#    assert board4.put_disc('black', 0, 1) == [(1, 1)]
#    assert board4.put_disc('white', 2, 0) == [(2, 1), (1, 0)]
#    assert board4.put_disc('black', 3, 0) == [(2, 1)]
#    assert board4.put_disc('white', 1, 3) == [(1, 2), (1, 1)]
#    assert board4.put_disc('black', 0, 3) == [(1, 2)]
#    assert board4.put_disc('white', 0, 2) == [(1, 2), (0, 1)]
#    assert board4.put_disc('black', 2, 3) == [(1, 3), (2, 2)]
#    assert board4.put_disc('white', 3, 2) == [(2, 2), (2, 1)]
#    assert board4.put_disc('black', 3, 1) == [(2, 2)]
#    assert board4.put_disc('white', 3, 3) == [(2, 2)]
#
#    assert board4.get_bitboard_info() == (4366, 61169)
#
#    # プレイ結果
#    print(board4)
#    board4_ret = [[board4.disc['blank'] for _ in range(4)] for _ in range(4)]
#    board4_ret[0][0] = board4.disc['white']
#    board4_ret[0][1] = board4.disc['white']
#    board4_ret[0][2] = board4.disc['white']
#    board4_ret[0][3] = board4.disc['black']
#    board4_ret[1][0] = board4.disc['white']
#    board4_ret[1][1] = board4.disc['white']
#    board4_ret[1][2] = board4.disc['white']
#    board4_ret[1][3] = board4.disc['black']
#    board4_ret[2][0] = board4.disc['white']
#    board4_ret[2][1] = board4.disc['white']
#    board4_ret[2][2] = board4.disc['white']
#    board4_ret[2][3] = board4.disc['white']
#    board4_ret[3][0] = board4.disc['black']
#    board4_ret[3][1] = board4.disc['black']
#    board4_ret[3][2] = board4.disc['black']
#    board4_ret[3][3] = board4.disc['white']
#    assert board4._board == board4_ret
#    assert board4.score['black'] == 5
#    assert board4.score['white'] == 11
#
#    print(board4.get_board_info())
#
#    # やり直し
#    board4 = Board(4)
#    board4.put_disc('black', 0, 1)
#    print(board4)
#    assert board4.score['black'] == 4
#    assert board4.score['white'] == 1
#    board4.undo()
#    print(board4)
#    assert board4.score['black'] == 2
#    assert board4.score['white'] == 2
#    board4.put_disc('white', 0, 2)
#    print(board4)
#    board4.undo()
#    print(board4)
#
#    # ============ #
#    # ビットボード #
#    # ============ #
#    bitboard4 = BitBoard(4)
#    bitboard8 = BitBoard(8)
#    bitboard10 = BitBoard(10)
#    bitboard20 = BitBoard(20)
#    bitboard26 = BitBoard(26)
#
#    # 初期位置
#    assert bitboard4._black_bitboard == 0x240
#    assert bitboard4._white_bitboard == 0x420
#    assert bitboard8._black_bitboard == 0x810000000
#    assert bitboard8._white_bitboard == 0x1008000000
#
#    # mask
#    assert bitboard4._mask.h == 0x6666
#    assert bitboard4._mask.v == 0x0FF0
#    assert bitboard4._mask.d == 0x0660
#    assert bitboard4._mask.u == 0xFFF0
#    assert bitboard4._mask.ur == 0x7770
#    assert bitboard4._mask.r == 0x7777
#    assert bitboard4._mask.br == 0x0777
#    assert bitboard4._mask.b == 0x0FFF
#    assert bitboard4._mask.bl == 0x0EEE
#    assert bitboard4._mask.l == 0xEEEE
#    assert bitboard4._mask.ul == 0xEEE0
#
#    assert bitboard8._mask.h == 0x7E7E7E7E7E7E7E7E
#    assert bitboard8._mask.v == 0x00FFFFFFFFFFFF00
#    assert bitboard8._mask.d == 0x007E7E7E7E7E7E00
#    assert bitboard8._mask.u == 0xFFFFFFFFFFFFFF00
#    assert bitboard8._mask.ur == 0x7F7F7F7F7F7F7F00
#    assert bitboard8._mask.r == 0x7F7F7F7F7F7F7F7F
#    assert bitboard8._mask.br == 0x007F7F7F7F7F7F7F
#    assert bitboard8._mask.b == 0x00FFFFFFFFFFFFFF
#    assert bitboard8._mask.bl == 0x00FEFEFEFEFEFEFE
#    assert bitboard8._mask.l == 0xFEFEFEFEFEFEFEFE
#    assert bitboard8._mask.ul == 0xFEFEFEFEFEFEFE00
#
#    # get_legal_moves
#    bitboard4._black_bitboard = 0x640
#    bitboard4._white_bitboard = 0x020
#    legal_moves = bitboard4.get_legal_moves('black')
#    assert legal_moves == {(3, 2): [(2, 2)], (2, 3): [(2, 2)], (3, 3): [(2, 2)]}
#    legal_moves = bitboard4.get_legal_moves('white')
#    assert legal_moves == {(0, 0): [(1, 1)], (2, 0): [(2, 1)], (0, 2): [(1, 2)]}
#
#    bitboard4._black_bitboard = 0x040
#    bitboard4._white_bitboard = 0x620
#    legal_moves = bitboard4.get_legal_moves('black')
#    assert legal_moves == {(1, 0): [(1, 1)], (3, 0): [(2, 1)], (3, 2): [(2, 2)]}
#    legal_moves = bitboard4.get_legal_moves('white')
#    assert legal_moves == {(0, 2): [(1, 2)], (0, 3): [(1, 2)], (1, 3): [(1, 2)]}
#
#    bitboard4._black_bitboard = 0x260
#    bitboard4._white_bitboard = 0x400
#    legal_moves = bitboard4.get_legal_moves('black')
#    assert legal_moves == {(0, 0): [(1, 1)], (1, 0): [(1, 1)], (0, 1): [(1, 1)]}
#    legal_moves = bitboard4.get_legal_moves('white')
#    assert legal_moves == {(3, 1): [(2, 1)], (1, 3): [(1, 2)], (3, 3): [(2, 2)]}
#
#    bitboard4._black_bitboard = 0x200
#    bitboard4._white_bitboard = 0x460
#    legal_moves = bitboard4.get_legal_moves('black')
#    assert legal_moves == {(0, 1): [(1, 1)], (0, 3): [(1, 2)], (2, 3): [(2, 2)]}
#    legal_moves = bitboard4.get_legal_moves('white')
#    assert legal_moves == {(2, 0): [(2, 1)], (3, 0): [(2, 1)], (3, 1): [(2, 1)]}
#
#    # put_disc
#    bitboard4._black_bitboard = 0x240
#    bitboard4._white_bitboard = 0x420
#
#    print('BitBoard')
#    print(bitboard4)
#    assert len(bitboard4.put_disc('black', 1, 0)) == 1
#    assert bitboard4.prev == [{'color': 'black', 'x': 1, 'y': 0, 'flippable_discs': 1024, 'disc_num': 1}]
#    assert len(bitboard4.put_disc('white', 0, 0)) == 1
#    assert bitboard4.prev == [{'color': 'black', 'x': 1, 'y': 0, 'flippable_discs': 1024, 'disc_num': 1}, {'color': 'white', 'x': 0, 'y': 0, 'flippable_discs': 1024, 'disc_num': 1}]
#    assert len(bitboard4.put_disc('black', 0, 1)) == 1
#    assert len(bitboard4.put_disc('white', 2, 0)) == 2
#    assert len(bitboard4.put_disc('black', 3, 2)) == 1
#    assert len(bitboard4.put_disc('white', 3, 3)) == 2
#    assert len(bitboard4.put_disc('black', 3, 1)) == 2
#    assert len(bitboard4.put_disc('white', 3, 0)) == 2
#    assert len(bitboard4.put_disc('black', 2, 3)) == 1
#    assert len(bitboard4.put_disc('white', 1, 3)) == 4
#    assert len(bitboard4.put_disc('black', 0, 3)) == 1
#    print(bitboard4)
#    assert len(bitboard4.put_disc('white', 0, 2)) == 2
#    print(bitboard4)
#
#    # score
#    assert bitboard4.score['black'] == 2
#    assert bitboard4.score['white'] == 14
#
#    # undo
#    bitboard4.undo()
#    assert bitboard4._black_bitboard == 0x0A48
#    assert bitboard4._white_bitboard == 0xF537
#    print(bitboard4)
#
#    # get_board_info
#    assert bitboard4.get_board_info() == [[-1, -1, -1, -1], [1, -1, 1, -1], [0, 1, -1, -1], [1, -1, -1, -1]]
#
#    # score
#    assert bitboard4.score['black'] == 4
#    assert bitboard4.score['white'] == 11
#
#    # size8
#    bitboard8 = BitBoard(8)
#    legal_moves = bitboard8.get_legal_moves('black')
#    assert legal_moves == {(3, 2): [(3, 3)], (2, 3): [(3, 3)], (5, 4): [(4, 4)], (4, 5): [(4, 4)]}
#
#    # 全般
#    bitboard8 = BitBoard(8)
#    bitboard8._black_bitboard = 0x0000240000240000
#    bitboard8._white_bitboard = 0x007E5A7A5E5A7E00
#    legal_moves = bitboard8.get_legal_moves('black')
#    assert legal_moves == {(0, 0): [(1, 1)], (2, 0): [(2, 1)], (3, 0): [(4, 1)], (4, 0): [(3, 1)], (5, 0): [(5, 1)], (7, 0): [(6, 1)], (0, 2): [(1, 2)], (7, 2): [(6, 2)], (0, 3): [(1, 4)], (5, 3): [(5, 4)], (7, 3): [(6, 4)], (0, 4): [(1, 3)], (2, 4): [(2, 3)], (7, 4): [(6, 3)], (0, 5): [(1, 5)], (7, 5): [(6, 5)], (0, 7): [(1, 6)], (2, 7): [(2, 6)], (3, 7): [(4, 6)], (4, 7): [(3, 6)], (5, 7): [(5, 6)], (7, 7): [(6, 6)]}
#
#    # 上黒
#    bitboard8 = BitBoard(8)
#    bitboard8._black_bitboard = 0x00000001000000BF
#    bitboard8._white_bitboard = 0x006573787C7E7F00
#    legal_moves = bitboard8.get_legal_moves('black')
#    assert legal_moves == {(0, 0): [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)], (2, 0): [(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6)], (4, 0): [(5, 1), (6, 2)], (7, 0): [(7, 1), (7, 2)], (0, 1): [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)], (3, 1): [(3, 2), (3, 3), (3, 4), (3, 5), (3, 6)], (0, 2): [(1, 3), (2, 4), (3, 5), (4, 6)], (4, 2): [(4, 3), (4, 4), (4, 5), (4, 6)], (5, 2): [(4, 3), (3, 4), (2, 5), (1, 6)], (0, 3): [(1, 4), (2, 5), (3, 6)], (5, 3): [(5, 4), (5, 5), (5, 6)], (6, 3): [(5, 4), (4, 5), (3, 6)], (0, 4): [(1, 5), (2, 6)], (6, 4): [(5, 5), (6, 5), (4, 6), (6, 6)], (7, 4): [(6, 5), (5, 6)], (0, 5): [(1, 6)], (7, 5): [(6, 6), (7, 6)]}
#
#    # 上白
#    bitboard8 = BitBoard(8)
#    bitboard8._black_bitboard = 0x00A6CE1E3E7EFE00
#    bitboard8._white_bitboard = 0x00000080000000FD
#    legal_moves = bitboard8.get_legal_moves('white')
#    assert legal_moves == {(0, 0): [(0, 1), (0, 2)], (3, 0): [(2, 1), (1, 2)], (5, 0): [(5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6)], (7, 0): [(6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6)], (4, 1): [(4, 2), (4, 3), (4, 4), (4, 5), (4, 6)], (7, 1): [(6, 2), (5, 3), (4, 4), (3, 5), (2, 6)], (2, 2): [(3, 3), (4, 4), (5, 5), (6, 6)], (3, 2): [(3, 3), (3, 4), (3, 5), (3, 6)], (7, 2): [(6, 3), (5, 4), (4, 5), (3, 6)], (1, 3): [(2, 4), (3, 5), (4, 6)], (2, 3): [(2, 4), (2, 5), (2, 6)], (7, 3): [(6, 4), (5, 5), (4, 6)], (0, 4): [(1, 5), (2, 6)], (1, 4): [(1, 5), (2, 5), (1, 6), (3, 6)], (7, 4): [(6, 5), (5, 6)], (0, 5): [(0, 6), (1, 6)], (7, 5): [(6, 6)]}
#
#    # 左黒
#    bitboard8 = BitBoard(8)
#    bitboard8._black_bitboard = 0x0100010101010111
#    bitboard8._white_bitboard = 0x007E7E3E1E4E2662
#    legal_moves = bitboard8.get_legal_moves('black')
#    assert legal_moves == {(0, 0): [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)], (1, 0): [(2, 1), (3, 2), (4, 3), (5, 4), (6, 5)], (2, 0): [(3, 1), (4, 2), (5, 3), (6, 4)], (3, 0): [(4, 1), (5, 2), (6, 3)], (4, 0): [(5, 1), (6, 2)], (5, 0): [(6, 1)], (0, 2): [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2)], (1, 3): [(2, 3), (3, 3), (4, 3), (5, 3), (6, 3)], (0, 4): [(1, 5), (2, 6)], (2, 4): [(3, 4), (4, 4), (5, 4), (6, 4)], (2, 5): [(6, 1), (5, 2), (4, 3), (3, 4)], (3, 5): [(4, 5), (5, 5), (6, 5)], (3, 6): [(6, 3), (5, 4), (4, 5)], (4, 6): [(6, 4), (5, 5), (5, 6), (6, 6)], (0, 7): [(1, 7), (2, 7)], (4, 7): [(6, 5), (5, 6)], (5, 7): [(6, 6), (6, 7)]}
#
#    # 下黒
#    bitboard8 = BitBoard(8)
#    bitboard8._black_bitboard = 0xBF00000001000000
#    bitboard8._white_bitboard = 0x007F7E7C78736500
#    legal_moves = bitboard8.get_legal_moves('black')
#    assert legal_moves == {(0, 2): [(1, 1)], (7, 2): [(6, 1), (7, 1)], (0, 3): [(2, 1), (1, 2)], (6, 3): [(4, 1), (6, 1), (5, 2), (6, 2)], (7, 3): [(5, 1), (6, 2)], (0, 4): [(3, 1), (2, 2), (1, 3)], (5, 4): [(5, 1), (5, 2), (5, 3)], (6, 4): [(3, 1), (4, 2), (5, 3)], (0, 5): [(4, 1), (3, 2), (2, 3), (1, 4)], (4, 5): [(4, 1), (4, 2), (4, 3), (4, 4)], (5, 5): [(1, 1), (2, 2), (3, 3), (4, 4)], (0, 6): [(5, 1), (4, 2), (3, 3), (2, 4), (1, 5)], (3, 6): [(3, 1), (3, 2), (3, 3), (3, 4), (3, 5)], (0, 7): [(6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6)], (2, 7): [(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6)], (4, 7): [(6, 5), (5, 6)], (7, 7): [(7, 5), (7, 6)]}
#
#    # 右黒
#    bitboard8 = BitBoard(8)
#    bitboard8._black_bitboard = 0x8000808080808088
#    bitboard8._white_bitboard = 0x007E7E7C78726446
#    legal_moves = bitboard8.get_legal_moves('black')
#    assert legal_moves == {(2, 0): [(1, 1)], (3, 0): [(2, 1), (1, 2)], (4, 0): [(3, 1), (2, 2), (1, 3)], (5, 0): [(4, 1), (3, 2), (2, 3), (1, 4)], (6, 0): [(5, 1), (4, 2), (3, 3), (2, 4), (1, 5)], (7, 0): [(6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6)], (7, 2): [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2)], (6, 3): [(1, 3), (2, 3), (3, 3), (4, 3), (5, 3)], (5, 4): [(1, 4), (2, 4), (3, 4), (4, 4)], (7, 4): [(6, 5), (5, 6)], (4, 5): [(1, 5), (2, 5), (3, 5)], (5, 5): [(1, 1), (2, 2), (3, 3), (4, 4)], (3, 6): [(1, 4), (2, 5), (1, 6), (2, 6)], (4, 6): [(1, 3), (2, 4), (3, 5)], (2, 7): [(1, 6), (1, 7)], (3, 7): [(1, 5), (2, 6)], (7, 7): [(5, 7), (6, 7)]}
#
#    # test1
#    bitboard8 = BitBoard(8)
#    bitboard8._black_bitboard = 0x0000000000081000
#    bitboard8._white_bitboard = 0x0000001C1C140000
#    legal_moves = bitboard8.get_legal_moves('black')
#    assert legal_moves == {(3, 2): [(3, 3), (3, 4), (3, 5)], (4, 2): [(4, 3), (4, 4)], (2, 3): [(3, 4)], (6, 3): [(5, 4)], (2, 5): [(3, 5)], (6, 5): [(5, 5)]}
#
#    # get_bitboard_info
#    assert bitboard8.get_bitboard_info() == (0x0000000000081000, 0x0000001C1C140000)
