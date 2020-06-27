"""Tests of board.py
"""

import unittest
from reversi.board import BoardSizeError, Board, BitBoard


class TestBoard(unittest.TestCase):
    """board
    """
    def test_board_size_2(self):
        err = False

        try:
            board = Board(2)
        except BoardSizeError as e:
            err = True

        self.assertTrue(err)

    def test_board_size_3(self):
        err = False

        try:
            board = Board(3)
        except BoardSizeError as e:
            err = True

        self.assertTrue(err)

    def test_board_size_28(self):
        err = False

        try:
            board = Board(28)
        except BoardSizeError as e:
            err = True

        self.assertTrue(err)

    def test_bitboard_size_2(self):
        err = False

        try:
            board = BitBoard(2)
        except BoardSizeError as e:
            err = True

        self.assertTrue(err)

    def test_bitboard_size_3(self):
        err = False

        try:
            board = BitBoard(3)
        except BoardSizeError as e:
            err = True

        self.assertTrue(err)

    def test_bitboard_size_28(self):
        err = False

        try:
            board = BitBoard(28)
        except BoardSizeError as e:
            err = True

        self.assertTrue(err)

    def test_board_size_4_initial(self):
        board = Board(4)

        board_ini = [[board.disc['blank'] for _ in range(4)] for _ in range(4)]
        board_ini[2][1] = board.disc['black']
        board_ini[1][2] = board.disc['black']
        board_ini[1][1] = board.disc['white']
        board_ini[2][2] = board.disc['white']

        self.assertEqual(board._board, board_ini)

    def test_board_size_6_initial(self):
        board = Board(6)

        board_ini = [[board.disc['blank'] for _ in range(6)] for _ in range(6)]
        board_ini[3][2] = board.disc['black']
        board_ini[2][3] = board.disc['black']
        board_ini[2][2] = board.disc['white']
        board_ini[3][3] = board.disc['white']

        self.assertEqual(board._board, board_ini)

    def test_board_size_8_initial(self):
        board = Board()

        board_ini = [[board.disc['blank'] for _ in range(8)] for _ in range(8)]
        board_ini[4][3] = board.disc['black']
        board_ini[3][4] = board.disc['black']
        board_ini[3][3] = board.disc['white']
        board_ini[4][4] = board.disc['white']

        self.assertEqual(board._board, board_ini)

    def test_board_size_10_initial(self):
        board = Board(10)

        board_ini = [[board.disc['blank'] for _ in range(10)] for _ in range(10)]
        board_ini[5][4] = board.disc['black']
        board_ini[4][5] = board.disc['black']
        board_ini[4][4] = board.disc['white']
        board_ini[5][5] = board.disc['white']

        self.assertEqual(board._board, board_ini)

    def test_board_size_26_initial(self):
        board = Board(26)

        board_ini = [[board.disc['blank'] for _ in range(26)] for _ in range(26)]
        board_ini[13][12] = board.disc['black']
        board_ini[12][13] = board.disc['black']
        board_ini[12][12] = board.disc['white']
        board_ini[13][13] = board.disc['white']

        self.assertEqual(board._board, board_ini)

    def test_bitboard_size_4_initial(self):
        board = BitBoard(4)
        self.assertEqual(board._black_bitboard, 0x240)
        self.assertEqual(board._white_bitboard, 0x420)

    def test_bitboard_size_6_initial(self):
        board = BitBoard(6)
        self.assertEqual(board._black_bitboard, 0x108000)
        self.assertEqual(board._white_bitboard, 0x204000)

    def test_bitboard_size_8_initial(self):
        board = BitBoard(8)
        self.assertEqual(board._black_bitboard, 0x810000000)
        self.assertEqual(board._white_bitboard, 0x1008000000)

    def test_bitboard_size_10_initial(self):
        board = BitBoard(10)
        self.assertEqual(board._black_bitboard, 0x40200000000000)
        self.assertEqual(board._white_bitboard, 0x80100000000000)

    def test_bitboard_size_26_initial(self):
        board = BitBoard(26)
        self.assertEqual(board._black_bitboard, 0x4000002000000000000000000000000000000000000000000000000000000000000000000000000000000000)
        self.assertEqual(board._white_bitboard, 0x8000001000000000000000000000000000000000000000000000000000000000000000000000000000000000)

    def test_board_size_4_put_disc(self):
        board = Board(4)
        self.assertEqual(board.put_disc('black', 0, 0), [])
        self.assertEqual(board.put_disc('black', 3, 5), [])
        self.assertEqual(board.put_disc('black', 1, 0), [(1, 1)])
        self.assertEqual(board.put_disc('white', 0, 0), [(1, 1)])
        self.assertEqual(board.put_disc('black', 0, 1), [(1, 1)])
        self.assertEqual(board.put_disc('white', 2, 0), [(2, 1), (1, 0)])
        self.assertEqual(board.put_disc('black', 3, 0), [(2, 1)])
        self.assertEqual(board.put_disc('white', 1, 3), [(1, 2), (1, 1)])
        self.assertEqual(board.put_disc('black', 0, 3), [(1, 2)])
        self.assertEqual(board.put_disc('white', 0, 2), [(1, 2), (0, 1)])
        self.assertEqual(board.put_disc('black', 2, 3), [(1, 3), (2, 2)])
        self.assertEqual(board.put_disc('white', 3, 2), [(2, 2), (2, 1)])
        self.assertEqual(board.put_disc('black', 3, 1), [(2, 2)])
        self.assertEqual(board.put_disc('white', 3, 3), [(2, 2)])
        self.assertEqual(board.get_bitboard_info(), (4366, 61169))

    def test_bitboard_size_4_put_disc(self):
        board = BitBoard(4)
        self.assertEqual(board.put_disc('black', 0, 0), [])
        self.assertEqual(board.put_disc('black', 3, 5), [])
        self.assertEqual(board.put_disc('black', 1, 0), [(1, 1)])
        self.assertEqual(board.put_disc('white', 0, 0), [(1, 1)])
        self.assertEqual(board.put_disc('black', 0, 1), [(1, 1)])
        self.assertEqual(board.put_disc('white', 2, 0), [(1, 0), (2, 1)])
        self.assertEqual(board.put_disc('black', 3, 0), [(2, 1)])
        self.assertEqual(board.put_disc('white', 1, 3), [(1, 1), (1, 2)])
        self.assertEqual(board.put_disc('black', 0, 3), [(1, 2)])
        self.assertEqual(board.put_disc('white', 0, 2), [(0, 1), (1, 2)])
        self.assertEqual(board.put_disc('black', 2, 3), [(2, 2), (1, 3)])
        self.assertEqual(board.put_disc('white', 3, 2), [(2, 1), (2, 2)])
        self.assertEqual(board.put_disc('black', 3, 1), [(2, 2)])
        self.assertEqual(board.put_disc('white', 3, 3), [(2, 2)])
        self.assertEqual(board.get_bitboard_info(), (4366, 61169))

    def test_board_size_8_play_result(self):
        board = Board()
        board.put_disc('black', 5, 4)
        board.put_disc('white', 5, 5)
        board.put_disc('black', 4, 5)
        board.put_disc('white', 3, 5)
        board.put_disc('black', 2, 6)
        board.put_disc('white', 5, 3)
        board.put_disc('black', 6, 2)
        board.put_disc('white', 3, 6)
        board.put_disc('black', 2, 2)

        board_str = """   a b c d e f g h
 1□□□□□□□□
 2□□□□□□□□
 3□□〇□□□〇□
 4□□□〇●〇□□
 5□□□●〇●□□
 6□□□●●●□□
 7□□〇●□□□□
 8□□□□□□□□
"""

        board_ret = [[board.disc['blank'] for _ in range(8)] for _ in range(8)]
        board_ret[2][2] = board.disc['black']
        board_ret[2][6] = board.disc['black']
        board_ret[3][3] = board.disc['black']
        board_ret[3][4] = board.disc['white']
        board_ret[3][5] = board.disc['black']
        board_ret[4][3] = board.disc['white']
        board_ret[4][4] = board.disc['black']
        board_ret[4][5] = board.disc['white']
        board_ret[5][3] = board.disc['white']
        board_ret[5][4] = board.disc['white']
        board_ret[5][5] = board.disc['white']
        board_ret[6][2] = board.disc['black']
        board_ret[6][3] = board.disc['white']

        board_info_ret = [[0 for _ in range(8)] for _ in range(8)]
        board_info_ret[2][2] = 1
        board_info_ret[2][6] = 1
        board_info_ret[3][3] = 1
        board_info_ret[3][4] = -1
        board_info_ret[3][5] = 1
        board_info_ret[4][3] = -1
        board_info_ret[4][4] = 1
        board_info_ret[4][5] = -1
        board_info_ret[5][3] = -1
        board_info_ret[5][4] = -1
        board_info_ret[5][5] = -1
        board_info_ret[6][2] = 1
        board_info_ret[6][3] = -1

        self.assertEqual(str(board), board_str)
        self.assertEqual(board._board, board_ret)
        self.assertEqual(board.get_board_info(), board_info_ret)
        self.assertEqual(board.get_bitboard_info(), (0x0000221408002000, 0x00000008141C1000))
        self.assertEqual(board.score['black'], 6)
        self.assertEqual(board.score['white'], 7)

    def test_bitboard_size_8_play_result(self):
        board = BitBoard()
        board.put_disc('black', 5, 4)
        board.put_disc('white', 5, 5)
        board.put_disc('black', 4, 5)
        board.put_disc('white', 3, 5)
        board.put_disc('black', 2, 6)
        board.put_disc('white', 5, 3)
        board.put_disc('black', 6, 2)
        board.put_disc('white', 3, 6)
        board.put_disc('black', 2, 2)

        board_str = """   a b c d e f g h
 1□□□□□□□□
 2□□□□□□□□
 3□□〇□□□〇□
 4□□□〇●〇□□
 5□□□●〇●□□
 6□□□●●●□□
 7□□〇●□□□□
 8□□□□□□□□
"""
        board_info_ret = [[0 for _ in range(8)] for _ in range(8)]
        board_info_ret[2][2] = 1
        board_info_ret[2][6] = 1
        board_info_ret[3][3] = 1
        board_info_ret[3][4] = -1
        board_info_ret[3][5] = 1
        board_info_ret[4][3] = -1
        board_info_ret[4][4] = 1
        board_info_ret[4][5] = -1
        board_info_ret[5][3] = -1
        board_info_ret[5][4] = -1
        board_info_ret[5][5] = -1
        board_info_ret[6][2] = 1
        board_info_ret[6][3] = -1

        self.assertEqual(str(board), board_str)
        self.assertEqual(board.get_board_info(), board_info_ret)
        self.assertEqual(board.get_bitboard_info(), (0x0000221408002000, 0x00000008141C1000))
        self.assertEqual(board.score['black'], 6)
        self.assertEqual(board.score['white'], 7)

    def test_board_size_8_undo(self):
        board = Board()
        board.put_disc('black', 5, 4)
        board.put_disc('white', 5, 5)
        board.put_disc('black', 4, 5)
        board.put_disc('white', 3, 5)
        board.put_disc('black', 2, 6)
        board.put_disc('white', 5, 3)
        board.put_disc('black', 6, 2)
        board.put_disc('white', 3, 6)
        board.put_disc('black', 2, 2)

        board_str = """   a b c d e f g h
 1□□□□□□□□
 2□□□□□□□□
 3□□〇□□□〇□
 4□□□〇●〇□□
 5□□□●〇●□□
 6□□□●●●□□
 7□□〇●□□□□
 8□□□□□□□□
"""
        self.assertEqual(str(board), board_str)

        board_str = """   a b c d e f g h
 1□□□□□□□□
 2□□□□□□□□
 3□□□□□□〇□
 4□□□●●〇□□
 5□□□●〇●□□
 6□□□●●●□□
 7□□〇●□□□□
 8□□□□□□□□
"""
        board.undo()
        self.assertEqual(str(board), board_str)

    def test_bitboard_size_8_undo(self):
        board = BitBoard()
        board.put_disc('black', 5, 4)
        board.put_disc('white', 5, 5)
        board.put_disc('black', 4, 5)
        board.put_disc('white', 3, 5)
        board.put_disc('black', 2, 6)
        board.put_disc('white', 5, 3)
        board.put_disc('black', 6, 2)
        board.put_disc('white', 3, 6)
        board.put_disc('black', 2, 2)

        board_str = """   a b c d e f g h
 1□□□□□□□□
 2□□□□□□□□
 3□□〇□□□〇□
 4□□□〇●〇□□
 5□□□●〇●□□
 6□□□●●●□□
 7□□〇●□□□□
 8□□□□□□□□
"""
        self.assertEqual(str(board), board_str)

        board_str = """   a b c d e f g h
 1□□□□□□□□
 2□□□□□□□□
 3□□□□□□〇□
 4□□□●●〇□□
 5□□□●〇●□□
 6□□□●●●□□
 7□□〇●□□□□
 8□□□□□□□□
"""
        board.undo()
        self.assertEqual(str(board), board_str)

    def test_bitboard_mask(self):
        board = BitBoard(4)
        self.assertEqual(board._mask.h, 0x6666)
        self.assertEqual(board._mask.v, 0x0FF0)
        self.assertEqual(board._mask.d, 0x0660)
        self.assertEqual(board._mask.u, 0xFFF0)
        self.assertEqual(board._mask.ur, 0x7770)
        self.assertEqual(board._mask.r, 0x7777)
        self.assertEqual(board._mask.br, 0x0777)
        self.assertEqual(board._mask.b, 0x0FFF)
        self.assertEqual(board._mask.bl, 0x0EEE)
        self.assertEqual(board._mask.l, 0xEEEE)
        self.assertEqual(board._mask.ul, 0xEEE0)

        board = BitBoard(8)
        self.assertEqual(board._mask.h, 0x7E7E7E7E7E7E7E7E)
        self.assertEqual(board._mask.v, 0x00FFFFFFFFFFFF00)
        self.assertEqual(board._mask.d, 0x007E7E7E7E7E7E00)
        self.assertEqual(board._mask.u, 0xFFFFFFFFFFFFFF00)
        self.assertEqual(board._mask.ur, 0x7F7F7F7F7F7F7F00)
        self.assertEqual(board._mask.r, 0x7F7F7F7F7F7F7F7F)
        self.assertEqual(board._mask.br, 0x007F7F7F7F7F7F7F)
        self.assertEqual(board._mask.b, 0x00FFFFFFFFFFFFFF)
        self.assertEqual(board._mask.bl, 0x00FEFEFEFEFEFEFE)
        self.assertEqual(board._mask.l, 0xFEFEFEFEFEFEFEFE)
        self.assertEqual(board._mask.ul, 0xFEFEFEFEFEFEFE00)

    def test_board_size_4_get_legal_moves(self):
        board = Board(4)
        blank, black, white = board.disc['blank'], board.disc['black'], board.disc['white']

        board._board = [
            [blank, blank, blank, blank],
            [blank, black, black, blank],
            [blank, black, white, blank],
            [blank, blank, blank, blank],
        ]
        legal_moves = board.get_legal_moves('black', force=True)
        self.assertEqual(legal_moves, {(3, 2): [(2, 2)], (2, 3): [(2, 2)], (3, 3): [(2, 2)]})
        legal_moves = board.get_legal_moves('white', force=True)
        self.assertEqual(legal_moves, {(0, 0): [(1, 1)], (2, 0): [(2, 1)], (0, 2): [(1, 2)]})

        board._board = [
            [blank, blank, blank, blank],
            [blank, white, white, blank],
            [blank, black, white, blank],
            [blank, blank, blank, blank],
        ]
        legal_moves = board.get_legal_moves('black', force=True)
        self.assertEqual(legal_moves, {(1, 0): [(1, 1)], (3, 0): [(2, 1)], (3, 2): [(2, 2)]})
        legal_moves = board.get_legal_moves('white', force=True)
        self.assertEqual(legal_moves, {(0, 2): [(1, 2)], (0, 3): [(1, 2)], (1, 3): [(1, 2)]})

        board._board = [
            [blank, blank, blank, blank],
            [blank, white, black, blank],
            [blank, black, black, blank],
            [blank, blank, blank, blank],
        ]
        legal_moves = board.get_legal_moves('black', force=True)
        self.assertEqual(legal_moves, {(0, 0): [(1, 1)], (1, 0): [(1, 1)], (0, 1): [(1, 1)]})
        legal_moves = board.get_legal_moves('white', force=True)
        self.assertEqual(legal_moves, {(3, 1): [(2, 1)], (1, 3): [(1, 2)], (3, 3): [(2, 2)]})

        board._board = [
            [blank, blank, blank, blank],
            [blank, white, black, blank],
            [blank, white, white, blank],
            [blank, blank, blank, blank],
        ]
        legal_moves = board.get_legal_moves('black', force=True)
        self.assertEqual(legal_moves, {(0, 1): [(1, 1)], (0, 3): [(1, 2)], (2, 3): [(2, 2)]})
        legal_moves = board.get_legal_moves('white', force=True)
        self.assertEqual(legal_moves, {(2, 0): [(2, 1)], (3, 0): [(2, 1)], (3, 1): [(2, 1)]})

    def test_board_size_8_get_legal_moves(self):
        board = Board(8)
        blank, black, white = board.disc['blank'], board.disc['black'], board.disc['white']
        legal_moves = board.get_legal_moves('black', force=True)
        self.assertEqual(legal_moves, {(3, 2): [(3, 3)], (2, 3): [(3, 3)], (5, 4): [(4, 4)], (4, 5): [(4, 4)]})

        # pattern1
        board._board = [
            [blank, blank, blank, blank, blank, blank, blank, blank],
            [blank, white, white, white, white, white, white, blank],
            [blank, white, black, white, white, black, white, blank],
            [blank, white, white, white, white, blank, white, blank],
            [blank, white, blank, white, white, white, white, blank],
            [blank, white, black, white, white, black, white, blank],
            [blank, white, white, white, white, white, white, blank],
            [blank, blank, blank, blank, blank, blank, blank, blank],
        ]
        legal_moves = board.get_legal_moves('black', force=True)
        self.assertEqual(legal_moves, {(0, 0): [(1, 1)], (2, 0): [(2, 1)], (3, 0): [(4, 1)], (4, 0): [(3, 1)], (5, 0): [(5, 1)], (7, 0): [(6, 1)], (0, 2): [(1, 2)], (7, 2): [(6, 2)], (0, 3): [(1, 4)], (5, 3): [(5, 4)], (7, 3): [(6, 4)], (0, 4): [(1, 3)], (2, 4): [(2, 3)], (7, 4): [(6, 3)], (0, 5): [(1, 5)], (7, 5): [(6, 5)], (0, 7): [(1, 6)], (2, 7): [(2, 6)], (3, 7): [(4, 6)], (4, 7): [(3, 6)], (5, 7): [(5, 6)], (7, 7): [(6, 6)]})

        # pattern2
        board._board = [
            [blank, blank, blank, blank, blank, blank, blank, blank],
            [blank, white, white, blank, blank, white, blank, white],
            [blank, white, white, white, blank, blank, white, white],
            [blank, white, white, white, white, blank, blank, black],
            [blank, white, white, white, white, white, blank, blank],
            [blank, white, white, white, white, white, white, blank],
            [blank, white, white, white, white, white, white, white],
            [black, blank, black, black, black, black, black, black],
        ]
        legal_moves = board.get_legal_moves('black', force=True)
        self.assertEqual(legal_moves, {(0, 0): [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)], (2, 0): [(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6)], (4, 0): [(5, 1), (6, 2)], (7, 0): [(7, 1), (7, 2)], (0, 1): [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)], (3, 1): [(3, 2), (3, 3), (3, 4), (3, 5), (3, 6)], (0, 2): [(1, 3), (2, 4), (3, 5), (4, 6)], (4, 2): [(4, 3), (4, 4), (4, 5), (4, 6)], (5, 2): [(4, 3), (3, 4), (2, 5), (1, 6)], (0, 3): [(1, 4), (2, 5), (3, 6)], (5, 3): [(5, 4), (5, 5), (5, 6)], (6, 3): [(5, 4), (4, 5), (3, 6)], (0, 4): [(1, 5), (2, 6)], (6, 4): [(5, 5), (4, 6), (6, 5), (6, 6)], (7, 4): [(6, 5), (5, 6)], (0, 5): [(1, 6)], (7, 5): [(6, 6), (7, 6)]})

        # pattern3
        board._board = [
            [blank, blank, blank, blank, blank, blank, blank, blank],
            [black, blank, black, blank, blank, black, black, blank],
            [black, black, blank, blank, black, black, black, blank],
            [white, blank, blank, black, black, black, black, blank],
            [blank, blank, black, black, black, black, black, blank],
            [blank, black, black, black, black, black, black, blank],
            [black, black, black, black, black, black, black, blank],
            [white, white, white, white, white, white, blank, white],
        ]
        legal_moves = board.get_legal_moves('white', force=True)
        self.assertEqual(legal_moves, {(0, 0): [(0, 1), (0, 2)], (3, 0): [(2, 1), (1, 2)], (5, 0): [(5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6)], (7, 0): [(6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6)], (4, 1): [(4, 2), (4, 3), (4, 4), (4, 5), (4, 6)], (7, 1): [(6, 2), (5, 3), (4, 4), (3, 5), (2, 6)], (2, 2): [(3, 3), (4, 4), (5, 5), (6, 6)], (3, 2): [(3, 3), (3, 4), (3, 5), (3, 6)], (7, 2): [(6, 3), (5, 4), (4, 5), (3, 6)], (1, 3): [(2, 4), (3, 5), (4, 6)], (2, 3): [(2, 4), (2, 5), (2, 6)], (7, 3): [(6, 4), (5, 5), (4, 6)], (0, 4): [(1, 5), (2, 6)], (1, 4): [(1, 5), (1, 6), (2, 5), (3, 6)], (7, 4): [(6, 5), (5, 6)], (0, 5): [(0, 6), (1, 6)], (7, 5): [(6, 6)]})

        # pattern4
        board._board = [
            [blank, blank, blank, blank, blank, blank, blank, black],
            [blank, white, white, white, white, white, white, blank],
            [blank, white, white, white, white, white, white, black],
            [blank, blank, white, white, white, white, white, black],
            [blank, blank, blank, white, white, white, white, black],
            [blank, white, blank, blank, white, white, white, black],
            [blank, blank, white, blank, blank, white, white, black],
            [blank, white, white, black, blank, blank, white, black],
        ]
        legal_moves = board.get_legal_moves('black', force=True)
        self.assertEqual(legal_moves, {(0, 0): [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)], (1, 0): [(2, 1), (3, 2), (4, 3), (5, 4), (6, 5)], (2, 0): [(3, 1), (4, 2), (5, 3), (6, 4)], (3, 0): [(4, 1), (5, 2), (6, 3)], (4, 0): [(5, 1), (6, 2)], (5, 0): [(6, 1)], (0, 2): [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2)], (1, 3): [(2, 3), (3, 3), (4, 3), (5, 3), (6, 3)], (0, 4): [(1, 5), (2, 6)], (2, 4): [(3, 4), (4, 4), (5, 4), (6, 4)], (2, 5): [(3, 4), (4, 3), (5, 2), (6, 1)], (3, 5): [(4, 5), (5, 5), (6, 5)], (3, 6): [(4, 5), (5, 4), (6, 3)], (4, 6): [(5, 6), (6, 6), (5, 5), (6, 4)], (0, 7): [(1, 7), (2, 7)], (4, 7): [(5, 6), (6, 5)], (5, 7): [(6, 7), (6, 6)]})

        # pattern5
        board._board = [
            [black, blank, black, black, black, black, black, black],
            [blank, white, white, white, white, white, white, white],
            [blank, white, white, white, white, white, white, blank],
            [blank, white, white, white, white, white, blank, blank],
            [blank, white, white, white, white, blank, blank, black],
            [blank, white, white, white, blank, blank, white, white],
            [blank, white, white, blank, blank, white, blank, white],
            [blank, blank, blank, blank, blank, blank, blank, blank],
        ]
        legal_moves = board.get_legal_moves('black', force=True)
        self.assertEqual(legal_moves, {(0, 2): [(1, 1)], (7, 2): [(6, 1), (7, 1)], (0, 3): [(1, 2), (2, 1)], (6, 3): [(5, 2), (4, 1), (6, 2), (6, 1)], (7, 3): [(6, 2), (5, 1)], (0, 4): [(1, 3), (2, 2), (3, 1)], (5, 4): [(5, 3), (5, 2), (5, 1)], (6, 4): [(5, 3), (4, 2), (3, 1)], (0, 5): [(1, 4), (2, 3), (3, 2), (4, 1)], (4, 5): [(4, 4), (4, 3), (4, 2), (4, 1)], (5, 5): [(4, 4), (3, 3), (2, 2), (1, 1)], (0, 6): [(1, 5), (2, 4), (3, 3), (4, 2), (5, 1)], (3, 6): [(3, 5), (3, 4), (3, 3), (3, 2), (3, 1)], (0, 7): [(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)], (2, 7): [(2, 6), (2, 5), (2, 4), (2, 3), (2, 2), (2, 1)], (4, 7): [(5, 6), (6, 5)], (7, 7): [(7, 6), (7, 5)]})

        # pattern6
        board._board = [
            [black, blank, blank, blank, blank, blank, blank, blank],
            [blank, white, white, white, white, white, white, blank],
            [black, white, white, white, white, white, white, blank],
            [black, white, white, white, white, white, blank, blank],
            [black, white, white, white, white, blank, blank, blank],
            [black, white, white, white, blank, blank, white, blank],
            [black, white, white, blank, blank, white, blank, blank],
            [black, white, blank, blank, black, white, white, blank],
        ]
        legal_moves = board.get_legal_moves('black', force=True)
        self.assertEqual(legal_moves, {(2, 0): [(1, 1)], (3, 0): [(2, 1), (1, 2)], (4, 0): [(3, 1), (2, 2), (1, 3)], (5, 0): [(4, 1), (3, 2), (2, 3), (1, 4)], (6, 0): [(5, 1), (4, 2), (3, 3), (2, 4), (1, 5)], (7, 0): [(6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6)], (7, 2): [(6, 2), (5, 2), (4, 2), (3, 2), (2, 2), (1, 2)], (6, 3): [(5, 3), (4, 3), (3, 3), (2, 3), (1, 3)], (5, 4): [(4, 4), (3, 4), (2, 4), (1, 4)], (7, 4): [(6, 5), (5, 6)], (4, 5): [(3, 5), (2, 5), (1, 5)], (5, 5): [(4, 4), (3, 3), (2, 2), (1, 1)], (3, 6): [(2, 6), (1, 6), (2, 5), (1, 4)], (4, 6): [(3, 5), (2, 4), (1, 3)], (2, 7): [(1, 7), (1, 6)], (3, 7): [(2, 6), (1, 5)], (7, 7): [(6, 7), (5, 7)]})

        # pattern7
        board._board = [
            [blank, blank, blank, blank, blank, blank, blank, blank],
            [blank, blank, blank, blank, blank, blank, blank, blank],
            [blank, blank, blank, blank, blank, blank, blank, blank],
            [blank, blank, blank, white, white, white, blank, blank],
            [blank, blank, blank, white, white, white, blank, blank],
            [blank, blank, blank, white, black, white, blank, blank],
            [blank, blank, blank, black, blank, blank, blank, blank],
            [blank, blank, blank, blank, blank, blank, blank, blank],
        ]
        legal_moves = board.get_legal_moves('black', force=True)
        self.assertEqual(legal_moves, {(3, 2): [(3, 3), (3, 4), (3, 5)], (4, 2): [(4, 3), (4, 4)], (2, 3): [(3, 4)], (6, 3): [(5, 4)], (2, 5): [(3, 5)], (6, 5): [(5, 5)]})

    def test_bitboard_size_4_get_legal_moves(self):
        board = BitBoard(4)

        board._black_bitboard = 0x640
        board._white_bitboard = 0x020
        legal_moves = board.get_legal_moves('black', force=True)
        self.assertEqual(legal_moves, {(3, 2): [(2, 2)], (2, 3): [(2, 2)], (3, 3): [(2, 2)]})
        legal_moves = board.get_legal_moves('white', force=True)
        self.assertEqual(legal_moves, {(0, 0): [(1, 1)], (2, 0): [(2, 1)], (0, 2): [(1, 2)]})

        board._black_bitboard = 0x040
        board._white_bitboard = 0x620
        legal_moves = board.get_legal_moves('black', force=True)
        self.assertEqual(legal_moves, {(1, 0): [(1, 1)], (3, 0): [(2, 1)], (3, 2): [(2, 2)]})
        legal_moves = board.get_legal_moves('white', force=True)
        self.assertEqual(legal_moves, {(0, 2): [(1, 2)], (0, 3): [(1, 2)], (1, 3): [(1, 2)]})

        board._black_bitboard = 0x260
        board._white_bitboard = 0x400
        legal_moves = board.get_legal_moves('black', force=True)
        self.assertEqual(legal_moves, {(0, 0): [(1, 1)], (1, 0): [(1, 1)], (0, 1): [(1, 1)]})
        legal_moves = board.get_legal_moves('white', force=True)
        self.assertEqual(legal_moves, {(3, 1): [(2, 1)], (1, 3): [(1, 2)], (3, 3): [(2, 2)]})

        board._black_bitboard = 0x200
        board._white_bitboard = 0x460
        legal_moves = board.get_legal_moves('black', force=True)
        self.assertEqual(legal_moves, {(0, 1): [(1, 1)], (0, 3): [(1, 2)], (2, 3): [(2, 2)]})
        legal_moves = board.get_legal_moves('white', force=True)
        self.assertEqual(legal_moves, {(2, 0): [(2, 1)], (3, 0): [(2, 1)], (3, 1): [(2, 1)]})

    def test_bitboard_size_8_get_legal_moves(self):
        board = BitBoard(8)
        legal_moves = board.get_legal_moves('black', force=True)
        self.assertEqual(legal_moves, {(3, 2): [(3, 3)], (2, 3): [(3, 3)], (5, 4): [(4, 4)], (4, 5): [(4, 4)]})

        # pattern1
        board._black_bitboard = 0x0000240000240000
        board._white_bitboard = 0x007E5A7A5E5A7E00
        legal_moves = board.get_legal_moves('black', force=True)
        self.assertEqual(legal_moves, {(0, 0): [(1, 1)], (2, 0): [(2, 1)], (3, 0): [(4, 1)], (4, 0): [(3, 1)], (5, 0): [(5, 1)], (7, 0): [(6, 1)], (0, 2): [(1, 2)], (7, 2): [(6, 2)], (0, 3): [(1, 4)], (5, 3): [(5, 4)], (7, 3): [(6, 4)], (0, 4): [(1, 3)], (2, 4): [(2, 3)], (7, 4): [(6, 3)], (0, 5): [(1, 5)], (7, 5): [(6, 5)], (0, 7): [(1, 6)], (2, 7): [(2, 6)], (3, 7): [(4, 6)], (4, 7): [(3, 6)], (5, 7): [(5, 6)], (7, 7): [(6, 6)]})

        # pattern2
        board._black_bitboard = 0x00000001000000BF
        board._white_bitboard = 0x006573787C7E7F00
        legal_moves = board.get_legal_moves('black', force=True)
        self.assertEqual(legal_moves, {(0, 0): [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)], (2, 0): [(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6)], (4, 0): [(5, 1), (6, 2)], (7, 0): [(7, 1), (7, 2)], (0, 1): [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)], (3, 1): [(3, 2), (3, 3), (3, 4), (3, 5), (3, 6)], (0, 2): [(1, 3), (2, 4), (3, 5), (4, 6)], (4, 2): [(4, 3), (4, 4), (4, 5), (4, 6)], (5, 2): [(4, 3), (3, 4), (2, 5), (1, 6)], (0, 3): [(1, 4), (2, 5), (3, 6)], (5, 3): [(5, 4), (5, 5), (5, 6)], (6, 3): [(5, 4), (4, 5), (3, 6)], (0, 4): [(1, 5), (2, 6)], (6, 4): [(5, 5), (6, 5), (4, 6), (6, 6)], (7, 4): [(6, 5), (5, 6)], (0, 5): [(1, 6)], (7, 5): [(6, 6), (7, 6)]})

        # pattern3
        board._black_bitboard = 0x00A6CE1E3E7EFE00
        board._white_bitboard = 0x00000080000000FD
        legal_moves = board.get_legal_moves('white', force=True)
        self.assertEqual(legal_moves, {(0, 0): [(0, 1), (0, 2)], (3, 0): [(2, 1), (1, 2)], (5, 0): [(5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6)], (7, 0): [(6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6)], (4, 1): [(4, 2), (4, 3), (4, 4), (4, 5), (4, 6)], (7, 1): [(6, 2), (5, 3), (4, 4), (3, 5), (2, 6)], (2, 2): [(3, 3), (4, 4), (5, 5), (6, 6)], (3, 2): [(3, 3), (3, 4), (3, 5), (3, 6)], (7, 2): [(6, 3), (5, 4), (4, 5), (3, 6)], (1, 3): [(2, 4), (3, 5), (4, 6)], (2, 3): [(2, 4), (2, 5), (2, 6)], (7, 3): [(6, 4), (5, 5), (4, 6)], (0, 4): [(1, 5), (2, 6)], (1, 4): [(1, 5), (2, 5), (1, 6), (3, 6)], (7, 4): [(6, 5), (5, 6)], (0, 5): [(0, 6), (1, 6)], (7, 5): [(6, 6)]})

        # pattern4
        board._black_bitboard = 0x0100010101010111
        board._white_bitboard = 0x007E7E3E1E4E2662
        legal_moves = board.get_legal_moves('black', force=True)
        self.assertEqual(legal_moves, {(0, 0): [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)], (1, 0): [(2, 1), (3, 2), (4, 3), (5, 4), (6, 5)], (2, 0): [(3, 1), (4, 2), (5, 3), (6, 4)], (3, 0): [(4, 1), (5, 2), (6, 3)], (4, 0): [(5, 1), (6, 2)], (5, 0): [(6, 1)], (0, 2): [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2)], (1, 3): [(2, 3), (3, 3), (4, 3), (5, 3), (6, 3)], (0, 4): [(1, 5), (2, 6)], (2, 4): [(3, 4), (4, 4), (5, 4), (6, 4)], (2, 5): [(6, 1), (5, 2), (4, 3), (3, 4)], (3, 5): [(4, 5), (5, 5), (6, 5)], (3, 6): [(6, 3), (5, 4), (4, 5)], (4, 6): [(6, 4), (5, 5), (5, 6), (6, 6)], (0, 7): [(1, 7), (2, 7)], (4, 7): [(6, 5), (5, 6)], (5, 7): [(6, 6), (6, 7)]})

        # pattern5
        board._black_bitboard = 0xBF00000001000000
        board._white_bitboard = 0x007F7E7C78736500
        legal_moves = board.get_legal_moves('black', force=True)
        self.assertEqual(legal_moves, {(0, 2): [(1, 1)], (7, 2): [(6, 1), (7, 1)], (0, 3): [(2, 1), (1, 2)], (6, 3): [(4, 1), (6, 1), (5, 2), (6, 2)], (7, 3): [(5, 1), (6, 2)], (0, 4): [(3, 1), (2, 2), (1, 3)], (5, 4): [(5, 1), (5, 2), (5, 3)], (6, 4): [(3, 1), (4, 2), (5, 3)], (0, 5): [(4, 1), (3, 2), (2, 3), (1, 4)], (4, 5): [(4, 1), (4, 2), (4, 3), (4, 4)], (5, 5): [(1, 1), (2, 2), (3, 3), (4, 4)], (0, 6): [(5, 1), (4, 2), (3, 3), (2, 4), (1, 5)], (3, 6): [(3, 1), (3, 2), (3, 3), (3, 4), (3, 5)], (0, 7): [(6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6)], (2, 7): [(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6)], (4, 7): [(6, 5), (5, 6)], (7, 7): [(7, 5), (7, 6)]})

        # pattern6
        board._black_bitboard = 0x8000808080808088
        board._white_bitboard = 0x007E7E7C78726446
        legal_moves = board.get_legal_moves('black', force=True)
        self.assertEqual(legal_moves, {(2, 0): [(1, 1)], (3, 0): [(2, 1), (1, 2)], (4, 0): [(3, 1), (2, 2), (1, 3)], (5, 0): [(4, 1), (3, 2), (2, 3), (1, 4)], (6, 0): [(5, 1), (4, 2), (3, 3), (2, 4), (1, 5)], (7, 0): [(6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6)], (7, 2): [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2)], (6, 3): [(1, 3), (2, 3), (3, 3), (4, 3), (5, 3)], (5, 4): [(1, 4), (2, 4), (3, 4), (4, 4)], (7, 4): [(6, 5), (5, 6)], (4, 5): [(1, 5), (2, 5), (3, 5)], (5, 5): [(1, 1), (2, 2), (3, 3), (4, 4)], (3, 6): [(1, 4), (2, 5), (1, 6), (2, 6)], (4, 6): [(1, 3), (2, 4), (3, 5)], (2, 7): [(1, 6), (1, 7)], (3, 7): [(1, 5), (2, 6)], (7, 7): [(5, 7), (6, 7)]})

        # pattern7
        board._black_bitboard = 0x0000000000081000
        board._white_bitboard = 0x0000001C1C140000
        legal_moves = board.get_legal_moves('black', force=True)
        self.assertEqual(legal_moves, {(3, 2): [(3, 3), (3, 4), (3, 5)], (4, 2): [(4, 3), (4, 4)], (2, 3): [(3, 4)], (6, 3): [(5, 4)], (2, 5): [(3, 5)], (6, 5): [(5, 5)]})
