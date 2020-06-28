"""Tests of scorer.py
"""

import unittest

from reversi.board import Board, BitBoard
import reversi.strategies.coordinator as coord


class TestScorer(unittest.TestCase):
    """scorer
    """
    def test_table_scorer(self):
        board = BitBoard()
        scorer = coord.TableScorer()

        # initial value
        self.assertEqual(scorer.table.size, 8)
        self.assertEqual(scorer.table._CORNER, 50)
        self.assertEqual(scorer.table._C, -20)
        self.assertEqual(scorer.table._A1, 0)
        self.assertEqual(scorer.table._A2, -1)
        self.assertEqual(scorer.table._B1, -1)
        self.assertEqual(scorer.table._B2, -1)
        self.assertEqual(scorer.table._B3, -1)
        self.assertEqual(scorer.table._X, -25)
        self.assertEqual(scorer.table._O1, -5)
        self.assertEqual(scorer.table._O2, -5)
        self.assertEqual(scorer.get_score('black', board), 0)
        self.assertEqual(scorer.get_score('white', board), 0)

        # b
        board.put_disc('black', 5, 4)
        self.assertEqual(scorer.get_score('black', board), -3)
        self.assertEqual(scorer.get_score('white', board), -3)

        # a1
        board.put_disc('white', 5, 5)
        self.assertEqual(scorer.get_score('black', board), -1)
        self.assertEqual(scorer.get_score('white', board), -1)

        # o
        board.put_disc('black', 5, 6)
        self.assertEqual(scorer.get_score('black', board), -6)
        self.assertEqual(scorer.get_score('white', board), -6)

        # x
        board.put_disc('white', 6, 6)
        self.assertEqual(scorer.get_score('black', board), 19)
        self.assertEqual(scorer.get_score('white', board), 19)

        # c
        board.put_disc('black', 7, 6)
        self.assertEqual(scorer.get_score('black', board), -51)
        self.assertEqual(scorer.get_score('white', board), -51)

        # corner
        board.put_disc('white', 7, 7)
        self.assertEqual(scorer.get_score('black', board), -51)
        self.assertEqual(scorer.get_score('white', board), -51)

        # a2
        board.put_disc('white', 5, 7)
        self.assertEqual(scorer.get_score('black', board), -40)
        self.assertEqual(scorer.get_score('white', board), -40)

    def test_possibility_scorer(self):
        board = Board()
        scorer = coord.PossibilityScorer()

        # initial value
        self.assertEqual(scorer._W, 5)
        black_moves = board.get_legal_moves('black', force=True)
        white_moves = board.get_legal_moves('white', force=True)
        self.assertEqual(scorer.get_score(black_moves, white_moves), 0)
        board.put_disc('black', 5, 4)
        black_moves = board.get_legal_moves('black', force=True)
        white_moves = board.get_legal_moves('white', force=True)
        self.assertEqual(scorer.get_score(black_moves, white_moves), 0)

        # check
        board = Board(8)
        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 2)
        board.put_disc('black', 2, 3)
        board.put_disc('white', 4, 2)
        board.put_disc('black', 1, 1)
        board.put_disc('white', 0, 0)

        black_moves = board.get_legal_moves('black', True)
        white_moves = board.get_legal_moves('white', True)

        self.assertEqual(scorer.get_score(black_moves, white_moves), 5)

    def test_opening_scorer(self):
        board = Board()
        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 2)
        board.put_disc('black', 2, 3)
        board.put_disc('white', 4, 2)
        board.put_disc('black', 1, 1)
        board.put_disc('white', 0, 0)

        scorer = coord.OpeningScorer()
        self.assertEqual(scorer.get_score(board), -8.25)

    def test_winlose_scorer(self):
        board = Board()
        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 2)
        board.put_disc('black', 2, 3)
        board.put_disc('white', 4, 2)
        board.put_disc('black', 1, 1)
        board.put_disc('white', 0, 0)

        scorer = coord.WinLoseScorer()
        self.assertEqual(scorer.get_score(board, [], []), -10006)

        black_moves = board.get_legal_moves('black', force=True)
        white_moves = board.get_legal_moves('white', force=True)
        self.assertEqual(scorer.get_score(board, black_moves, white_moves), None)

    def test_number_scorer(self):
        board = Board()
        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 2)
        board.put_disc('black', 2, 3)
        board.put_disc('white', 4, 2)
        board.put_disc('black', 1, 1)
        board.put_disc('white', 0, 0)

        scorer = coord.NumberScorer()
        self.assertEqual(scorer.get_score(board), -6)

    def test_edge_scorer(self):
        board = BitBoard()
        scorer = coord.EdgeScorer()

        # stable disc
        board._black_bitboard = 0xC000000000000000
        board._white_bitboard = 0x0000000000000000
        score = scorer.get_score(board)
        self.assertEqual(score, 100)

        board._black_bitboard = 0xE000000000000000
        board._white_bitboard = 0x0000000000000000
        score = scorer.get_score(board)
        self.assertEqual(score, 200)

        board._black_bitboard = 0xFF00000000000000
        board._white_bitboard = 0x0000000000000000
        score = scorer.get_score(board)
        self.assertEqual(score, 1300)

        board._black_bitboard = 0xFF818181818181FF
        board._white_bitboard = 0x0000000000000000
        score = scorer.get_score(board)
        self.assertEqual(score, 5200)

        board._black_bitboard = 0x0000000000000000
        board._white_bitboard = 0xC3810000000081C3
        score = scorer.get_score(board)
        self.assertEqual(score, -800)

        board._black_bitboard = 0x0000000000000000
        board._white_bitboard = 0xF7810080800081FF
        score = scorer.get_score(board)
        self.assertEqual(score, -2200)

    def test_corner_scorer(self):
        board = BitBoard(8)
        scorer = coord.CornerScorer()

        # Level1
        board._black_bitboard = 0x0000000000000000
        board._white_bitboard = 0x0000000000000000
        score = scorer.get_score(board)
        self.assertEqual(score, 0)
        board._black_bitboard = 0xE7C380000080C0C0
        board._white_bitboard = 0x0000000000010303
        score = scorer.get_score(board)
        self.assertEqual(score, 200)

        # Level2
        board._black_bitboard = 0x0000000080C0E0F0
        board._white_bitboard = 0xF7E703010000070F
        score = scorer.get_score(board)
        self.assertEqual(score, -400)

        # Level3
        board._black_bitboard = 0x00000080C0E0F0F8
        board._white_bitboard = 0x0303030301000000
        score = scorer.get_score(board)
        self.assertEqual(score, 300)
        board._black_bitboard = 0x0000000103070707
        board._white_bitboard = 0xF8F0C00000000000
        score = scorer.get_score(board)
        self.assertEqual(score, 100)

        # Level4
        board._black_bitboard = 0xF08080C0E0F0F8FD
        board._white_bitboard = 0x0F0F070703010000
        score = scorer.get_score(board)
        self.assertEqual(score, 100)
        board._black_bitboard = 0xFCF8000000C0F8FC
        board._white_bitboard = 0x0303030303010000
        score = scorer.get_score(board)
        self.assertEqual(score, 400)

        # Level5
        board._black_bitboard = 0xFFFCF8F0E0C08000
        board._white_bitboard = 0x0000000000000000
        score = scorer.get_score(board)
        self.assertEqual(score, 900)
        board._black_bitboard = 0x0000000000000000
        board._white_bitboard = 0x0F0F0F0F07030100
        score = scorer.get_score(board)
        self.assertEqual(score, -900)
        board._black_bitboard = 0xFFFEFCF8F0000000
        board._white_bitboard = 0x000000000F1F3F7F
        score = scorer.get_score(board)
        self.assertEqual(score, 0)
