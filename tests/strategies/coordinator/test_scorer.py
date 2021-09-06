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
        self.assertEqual(scorer.get_score('black', board, None, None), 0)
        self.assertEqual(scorer.get_score('white', board, None, None), 0)

        # b
        board.put_disc('black', 5, 4)
        self.assertEqual(scorer.get_score('black', board, None, None), -3)
        self.assertEqual(scorer.get_score('white', board, None, None), -3)

        # a1
        board.put_disc('white', 5, 5)
        self.assertEqual(scorer.get_score('black', board, None, None), -1)
        self.assertEqual(scorer.get_score('white', board, None, None), -1)

        # o
        board.put_disc('black', 5, 6)
        self.assertEqual(scorer.get_score('black', board, None, None), -6)
        self.assertEqual(scorer.get_score('white', board, None, None), -6)

        # x
        board.put_disc('white', 6, 6)
        self.assertEqual(scorer.get_score('black', board, None, None), 19)
        self.assertEqual(scorer.get_score('white', board, None, None), 19)

        # c
        board.put_disc('black', 7, 6)
        self.assertEqual(scorer.get_score('black', board, None, None), -51)
        self.assertEqual(scorer.get_score('white', board, None, None), -51)

        # corner
        board.put_disc('white', 7, 7)
        self.assertEqual(scorer.get_score('black', board, None, None), -51)
        self.assertEqual(scorer.get_score('white', board, None, None), -51)

        # a2
        board.put_disc('white', 5, 7)
        self.assertEqual(scorer.get_score('black', board, None, None), -40)
        self.assertEqual(scorer.get_score('white', board, None, None), -40)

    def test_possibility_scorer(self):
        board = Board()
        scorer = coord.PossibilityScorer()

        # initial value
        self.assertEqual(scorer._W, 5)
        possibility_b = board.get_bit_count(board.get_legal_moves_bits('black'))
        possibility_w = board.get_bit_count(board.get_legal_moves_bits('white'))
        self.assertEqual(scorer.get_score(None, None, possibility_b, possibility_w), 0)
        board.put_disc('black', 5, 4)
        possibility_b = board.get_bit_count(board.get_legal_moves_bits('black'))
        possibility_w = board.get_bit_count(board.get_legal_moves_bits('white'))
        self.assertEqual(scorer.get_score(None, None, possibility_b, possibility_w), 0)

        # check
        board = Board(8)
        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 2)
        board.put_disc('black', 2, 3)
        board.put_disc('white', 4, 2)
        board.put_disc('black', 1, 1)
        board.put_disc('white', 0, 0)

        possibility_b = board.get_bit_count(board.get_legal_moves_bits('black'))
        possibility_w = board.get_bit_count(board.get_legal_moves_bits('white'))

        self.assertEqual(scorer.get_score(None, None, possibility_b, possibility_w), 5)

    def test_opening_scorer(self):
        board = Board()
        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 2)
        board.put_disc('black', 2, 3)
        board.put_disc('white', 4, 2)
        board.put_disc('black', 1, 1)
        board.put_disc('white', 0, 0)

        scorer = coord.OpeningScorer()
        self.assertEqual(scorer.get_score(None, board, None, None), -8.25)

    def test_winlose_scorer(self):
        board = Board()
        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 2)
        board.put_disc('black', 2, 3)
        board.put_disc('white', 4, 2)
        board.put_disc('black', 1, 1)
        board.put_disc('white', 0, 0)

        scorer = coord.WinLoseScorer()
        self.assertEqual(scorer.get_score(None, board, None, None), -10006)

        possibility_b = board.get_legal_moves('black')
        possibility_w = board.get_legal_moves('white')
        self.assertEqual(scorer.get_score(None, board, possibility_b, possibility_w), None)

    def test_number_scorer(self):
        board = Board()
        board.put_disc('black', 3, 2)
        board.put_disc('white', 2, 2)
        board.put_disc('black', 2, 3)
        board.put_disc('white', 4, 2)
        board.put_disc('black', 1, 1)
        board.put_disc('white', 0, 0)

        scorer = coord.NumberScorer()
        self.assertEqual(scorer.get_score(None, board, None, None), -6)

    def test_edge_scorer(self):
        board = BitBoard()
        scorer = coord.EdgeScorer()

        # stable disc
        board._black_bitboard = 0xC000000000000000
        board._white_bitboard = 0x0000000000000000
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 100)

        board._black_bitboard = 0xE000000000000000
        board._white_bitboard = 0x0000000000000000
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 200)

        board._black_bitboard = 0xFF00000000000000
        board._white_bitboard = 0x0000000000000000
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 1300)

        board._black_bitboard = 0xFF818181818181FF
        board._white_bitboard = 0x0000000000000000
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 5200)

        board._black_bitboard = 0x0000000000000000
        board._white_bitboard = 0xC3810000000081C3
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, -800)

        board._black_bitboard = 0x0000000000000000
        board._white_bitboard = 0xF7810080800081FF
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, -2200)

        # board size is not 8
        board = BitBoard(4)
        board.put_disc('black', 0, 0)
        board.put_disc('white', 1, 0)
        board.put_disc('black', 0, 1)
        board.put_disc('white', 0, 2)
        board.put_disc('black', 0, 3)
        board.put_disc('white', 2, 0)
        board.put_disc('black', 3, 1)
        board.put_disc('white', 1, 3)
        board.put_disc('black', 3, 3)
        board.put_disc('white', 3, 0)
        board.put_disc('black', 2, 3)
        board.put_disc('white', 3, 2)
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 600)

    def test_corner_scorer(self):
        board = BitBoard(8)
        scorer = coord.CornerScorer()

        # Level1
        board._black_bitboard = 0x0000000000000000
        board._white_bitboard = 0x0000000000000000
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 0)
        board._black_bitboard = 0xE7C380000080C0C0
        board._white_bitboard = 0x0000000000010303
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 200)

        # Level2
        board._black_bitboard = 0x0000000080C0E0F0
        board._white_bitboard = 0xF7E703010000070F
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, -400)

        # Level3
        board._black_bitboard = 0x00000080C0E0F0F8
        board._white_bitboard = 0x0303030301000000
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 300)
        board._black_bitboard = 0x0000000103070707
        board._white_bitboard = 0xF8F0C00000000000
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 100)

        # Level4
        board._black_bitboard = 0xF08080C0E0F0F8FD
        board._white_bitboard = 0x0F0F070703010000
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 100)
        board._black_bitboard = 0xFCF8000000C0F8FC
        board._white_bitboard = 0x0303030303010000
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 400)

        # Level5
        board._black_bitboard = 0xFFFCF8F0E0C08000
        board._white_bitboard = 0x0000000000000000
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 900)
        board._black_bitboard = 0x0000000000000000
        board._white_bitboard = 0x0F0F0F0F07030100
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, -900)
        board._black_bitboard = 0xFFFEFCF8F0000000
        board._white_bitboard = 0x000000000F1F3F7F
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 0)

        # board size is not 8
        board = BitBoard(4)
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 0)

    def test_blank_scorer(self):
        board = BitBoard(8)
        scorer = coord.BlankScorer()

        # initial
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 0)

        # test1
        board.put_disc('black', 5, 4)
        board.put_disc('white', 5, 3)
        board.put_disc('black', 3, 2)
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, -20)

        # test2
        board.undo()
        board.put_disc('black', 2, 2)
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, -16)

        # test3
        board.undo()
        board.put_disc('black', 4, 2)
        board.put_disc('white', 5, 5)
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 8)

        # test4(left-top)
        board._black_bitboard = 0x2058082010000000
        board._white_bitboard = 0x4020101C0C040000
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 1)

        # test5(right-bottom)
        board._black_bitboard = 0x20583E3C1C060200
        board._white_bitboard = 0x4020000000000000
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, -53)

        # test6(right-top)
        board._black_bitboard = 0x007A562C7C060200
        board._white_bitboard = 0xFA84A8D080000000
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, -42)

        # test7(left-bottom)
        board._black_bitboard = 0x043A170C14320000
        board._white_bitboard = 0xFAC4E8F1E8CCC241
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 8)

    def test_edgecorner_scorer(self):
        board = BitBoard(8)
        scorer = coord.EdgeCornerScorer()

        # initial
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 0)

        # test1(left-bottom)
        board._black_bitboard = 0x00041800242014E0
        board._white_bitboard = 0x0000201C08182808
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 16)

        # test2(left-top)
        board._black_bitboard = 0x8084B8D6AFDCFEFC
        board._white_bitboard = 0x0000442850200000
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 24)

        # test3(right-bottom)
        board._black_bitboard = 0x1817A3DDADF4FBFF
        board._white_bitboard = 0x20886C22620A0400
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 24)

        # test4(right-top)
        board._black_bitboard = 0x1815E3DDADF4FBFF
        board._white_bitboard = 0x210A1C22520A0400
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 8)

        # test5(minus)
        board._black_bitboard = 0x1A16828CB6FAFCFC
        board._white_bitboard = 0x21497D7349050301
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, -8)

    def test_scorer_force_import_error(self):
        import os
        import importlib
        import reversi

        # -------------------------------
        # switch environ and reload module
        os.environ['FORCE_SCORERMETHODS_IMPORT_ERROR'] = 'RAISE'
        importlib.reload(reversi.strategies.coordinator.ScorerMethods)
        self.assertTrue(reversi.strategies.coordinator.ScorerMethods.SLOW_MODE)
        # -------------------------------

        # BlankScorer
        board = BitBoard(8)
        scorer = coord.BlankScorer()

        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 0)

        board.put_disc('black', 5, 4)
        board.put_disc('white', 5, 3)
        board.put_disc('black', 3, 2)
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, -20)

        board.undo()
        board.put_disc('black', 2, 2)
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, -16)

        board.undo()
        board.put_disc('black', 4, 2)
        board.put_disc('white', 5, 5)
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 8)

        board._black_bitboard = 0x2058082010000000
        board._white_bitboard = 0x4020101C0C040000
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 1)

        board._black_bitboard = 0x20583E3C1C060200
        board._white_bitboard = 0x4020000000000000
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, -53)

        board._black_bitboard = 0x007A562C7C060200
        board._white_bitboard = 0xFA84A8D080000000
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, -42)

        board._black_bitboard = 0x043A170C14320000
        board._white_bitboard = 0xFAC4E8F1E8CCC241
        score = scorer.get_score(None, board, None, None)
        self.assertEqual(score, 8)

        # -------------------------------
        # recover environment and reload module
        del os.environ['FORCE_SCORERMETHODS_IMPORT_ERROR']
        importlib.reload(reversi.strategies.coordinator.ScorerMethods)
        self.assertFalse(reversi.strategies.coordinator.ScorerMethods.SLOW_MODE)
        # -------------------------------
