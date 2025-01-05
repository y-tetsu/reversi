"""Tests of evaluator.py
"""

import unittest

from reversi.board import BitBoard
import reversi.strategies.coordinator as coord


class TestEvaluator(unittest.TestCase):
    """evaluator
    """
    def test_general_evaluator_init(self):
        evaluator = coord.Evaluator()
        self.assertEqual(evaluator.separated, [])
        self.assertEqual(evaluator.combined, [])

        separated = [coord.WinLoseScorer()]
        combined = [coord.PossibilityScorer(), coord.EdgeScorer()]
        evaluator = coord.Evaluator(separated=separated, combined=combined)
        self.assertEqual(evaluator.separated, separated)
        self.assertEqual(evaluator.combined, combined)

    def test_general_evaluator_evaluate(self):
        evaluator = coord.Evaluator(
            separated=[
                coord.WinLoseScorer(),
            ],
            combined=[
                coord.TableScorer(),
                coord.PossibilityScorer(),
                coord.EdgeScorer(),
            ],
        )

        board8 = BitBoard(8)
        board8._black_bitboard = 0xFFFFFFFFFFFFFFFF  # black win
        board8._white_bitboard = 0x0000000000000000
        board8.update_score()
        possibility_b = board8.get_bit_count(board8.get_legal_moves_bits('black'))
        possibility_w = board8.get_bit_count(board8.get_legal_moves_bits('white'))
        score_b = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        score_w = evaluator.evaluate('white', board8, possibility_b, possibility_w)
        self.assertEqual(score_b, 10064)
        self.assertEqual(score_w, 10064)

        board8._black_bitboard = 0x0000000000000000
        board8._white_bitboard = 0xFFFFFFFFFFFFFFFF  # white win
        board8.update_score()
        possibility_b = board8.get_bit_count(board8.get_legal_moves_bits('black'))
        possibility_w = board8.get_bit_count(board8.get_legal_moves_bits('white'))
        score_b = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        score_w = evaluator.evaluate('white', board8, possibility_b, possibility_w)
        self.assertEqual(score_b, -10064)
        self.assertEqual(score_w, -10064)

        board8 = BitBoard(8)
        board8.put_disc('black', 3, 2)
        board8.put_disc('white', 2, 2)
        board8.put_disc('black', 2, 3)
        board8.put_disc('white', 4, 2)
        board8.put_disc('black', 1, 1)
        board8.put_disc('white', 0, 0)
        board8._black_bitboard = 0x0000002010003C7E
        possibility_b = board8.get_bit_count(board8.get_legal_moves_bits('black'))
        possibility_w = board8.get_bit_count(board8.get_legal_moves_bits('white'))
        score = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score, -81)

        board8._black_bitboard = 0x0000002010003C7C
        score = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score, -61)

    def test_specific_evaluator(self):
        board8 = BitBoard(8)
        board8.put_disc('black', 3, 2)
        board8.put_disc('white', 2, 2)
        board8.put_disc('black', 2, 3)
        board8.put_disc('white', 4, 2)
        board8.put_disc('black', 1, 1)
        board8.put_disc('white', 0, 0)

        possibility_b = board8.get_bit_count(board8.get_legal_moves_bits('black'))
        possibility_w = board8.get_bit_count(board8.get_legal_moves_bits('white'))

        # Evaluator_T
        evaluator = coord.Evaluator_T()
        score_b = evaluator.evaluate('black', board8, None, None)
        score_w = evaluator.evaluate('white', board8, None, None)
        self.assertEqual(score_b, -22)
        self.assertEqual(score_w, -22)

        # Evaluator_P
        evaluator = coord.Evaluator_P()
        score_b = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score_b, 5)

        # Evaluator_O
        evaluator = coord.Evaluator_O()
        score_b = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score_b, -8.25)

        # Evaluator_W
        evaluator = coord.Evaluator_W()

        board8._black_bitboard = 0xFFFFFFFFFFFFFFFF  # black win
        board8._white_bitboard = 0x0000000000000000
        board8.update_score()
        possibility_b = board8.get_bit_count(board8.get_legal_moves_bits('black'))
        possibility_w = board8.get_bit_count(board8.get_legal_moves_bits('white'))
        score_b = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        score_w = evaluator.evaluate('white', board8, possibility_b, possibility_w)
        self.assertEqual(score_b, 10064)
        self.assertEqual(score_w, 10064)

        board8._black_bitboard = 0x0000000000000000
        board8._white_bitboard = 0xFFFFFFFFFFFFFFFF  # white win
        board8.update_score()
        possibility_b = board8.get_bit_count(board8.get_legal_moves_bits('black'))
        possibility_w = board8.get_bit_count(board8.get_legal_moves_bits('white'))
        score_b = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        score_w = evaluator.evaluate('white', board8, possibility_b, possibility_w)
        self.assertEqual(score_b, -10064)
        self.assertEqual(score_w, -10064)

        # Evaluator_N
        board8 = BitBoard(8)
        board8.put_disc('black', 3, 2)
        board8.put_disc('white', 2, 2)
        board8.put_disc('black', 2, 3)
        board8.put_disc('white', 4, 2)
        board8.put_disc('black', 1, 1)
        board8.put_disc('white', 0, 0)

        possibility_b = board8.get_bit_count(board8.get_legal_moves_bits('black'))
        possibility_w = board8.get_bit_count(board8.get_legal_moves_bits('white'))

        evaluator = coord.Evaluator_N()
        score_b = evaluator.evaluate('black', board8, None, None)
        self.assertEqual(score_b, -6)

        # Evaluator_N_Fast
        evaluator = coord.Evaluator_N_Fast()
        score_b = evaluator.evaluate('black', board8, None, None)
        self.assertEqual(score_b, -6)

        # Evaluator_E
        evaluator = coord.Evaluator_E()
        score_b = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score_b, 0)

        # Evaluator_C
        evaluator = coord.Evaluator_C()
        score_b = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score_b, 0)

        # Evaluator_B
        evaluator = coord.Evaluator_B()
        score_b = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score_b, 19)

        # Evaluator_Ec
        evaluator = coord.Evaluator_Ec()
        score_b = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score_b, -16)

        # Evaluator_TP
        evaluator = coord.Evaluator_TP()
        score_b = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score_b, -17)

        # Evaluator_TPO
        evaluator = coord.Evaluator_TPO()
        score_b = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score_b, -25.25)

        # Evaluator_NW
        evaluator = coord.Evaluator_NW()
        score = evaluator.evaluate(None, board8, None, None)
        self.assertEqual(score, -10006)
        score = evaluator.evaluate(None, board8, possibility_b, possibility_w)
        self.assertEqual(score, -6)

        # Evaluator_PW
        evaluator = coord.Evaluator_PW()
        score = evaluator.evaluate(None, board8, None, None)
        self.assertEqual(score, -10006)
        score = evaluator.evaluate(None, board8, possibility_b, possibility_w)
        self.assertEqual(score, 5)

        # Evaluator_TPW
        evaluator = coord.Evaluator_TPW()
        score = evaluator.evaluate(None, board8, None, None)
        self.assertEqual(score, -10006)
        score = evaluator.evaluate(None, board8, possibility_b, possibility_w)
        self.assertEqual(score, -17)

        # Evaluator_TPW_Fast
        board8 = BitBoard(8)
        board8.put_disc('black', 3, 2)
        board8.put_disc('white', 2, 2)
        board8.put_disc('black', 2, 3)
        board8.put_disc('white', 4, 2)
        board8.put_disc('black', 1, 1)

        possibility_b = board8.get_bit_count(board8.get_legal_moves_bits('black'))
        possibility_w = board8.get_bit_count(board8.get_legal_moves_bits('white'))

        evaluator = coord.Evaluator_TPW_Fast()
        score = evaluator.evaluate(None, board8, None, None)
        self.assertEqual(score, 10001)

        board8.put_disc('white', 0, 0)

        possibility_b = board8.get_bit_count(board8.get_legal_moves_bits('black'))
        possibility_w = board8.get_bit_count(board8.get_legal_moves_bits('white'))

        score = evaluator.evaluate(None, board8, None, None)
        self.assertEqual(score, -10006)
        score = evaluator.evaluate(None, board8, possibility_b, possibility_w)
        self.assertEqual(score, -17)

        # Evaluator_TPOW
        evaluator = coord.Evaluator_TPOW()
        score_b = evaluator.evaluate('black', board8, None, None)
        self.assertEqual(score_b, -10006)
        score_b = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score_b, -25.25)

        # Evaluator_TPWE
        evaluator = coord.Evaluator_TPWE()
        board8._black_bitboard = 0x0000002010003C7E
        possibility_b = board8.get_bit_count(board8.get_legal_moves_bits('black'))
        possibility_w = board8.get_bit_count(board8.get_legal_moves_bits('white'))
        score = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score, -81)

        board8._black_bitboard = 0x0000002010003C7C
        score = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score, -61)

        score = evaluator.evaluate('black', board8, None, None)
        self.assertEqual(score, -10006)

        # Evaluator_TPWE_Fast
        board8 = BitBoard(8)
        board8.put_disc('black', 3, 2)
        board8.put_disc('white', 2, 2)
        board8.put_disc('black', 2, 3)
        board8.put_disc('white', 4, 2)
        board8.put_disc('black', 1, 1)

        possibility_b = board8.get_bit_count(board8.get_legal_moves_bits('black'))
        possibility_w = board8.get_bit_count(board8.get_legal_moves_bits('white'))

        evaluator = coord.Evaluator_TPWE_Fast()
        score = evaluator.evaluate(None, board8, None, None)
        self.assertEqual(score, 10001)

        board8.put_disc('white', 0, 0)

        board8._black_bitboard = 0x0000002010003C7E
        possibility_b = board8.get_bit_count(board8.get_legal_moves_bits('black'))
        possibility_w = board8.get_bit_count(board8.get_legal_moves_bits('white'))
        score = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score, -81)

        board8._black_bitboard = 0x0000002010003C7C
        score = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score, -61)

        score = evaluator.evaluate('black', board8, None, None)
        self.assertEqual(score, -10006)

        board4 = BitBoard(4)
        possibility_b = board4.get_bit_count(board4.get_legal_moves_bits('black'))
        possibility_w = board4.get_bit_count(board4.get_legal_moves_bits('white'))
        score = evaluator.evaluate('black', board4, possibility_b, possibility_w)
        self.assertEqual(score, 0)

        # -------------------------------

        # Evaluator_TPWEC
        evaluator = coord.Evaluator_TPWEC()
        board8._black_bitboard = 0x0000002010003C7C
        possibility_b = board8.get_bit_count(board8.get_legal_moves_bits('black'))
        possibility_w = board8.get_bit_count(board8.get_legal_moves_bits('white'))
        score = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score, -61)
        board8._black_bitboard = 0x0703012010003C7E
        score = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score, 422)

        score = evaluator.evaluate('black', board8, None, None)
        self.assertEqual(score, -10006)

        # Evaluator_PWE
        evaluator = coord.Evaluator_PWE()
        board8._black_bitboard = 0x0000002010003C7C
        possibility_b = board8.get_bit_count(board8.get_legal_moves_bits('black'))
        possibility_w = board8.get_bit_count(board8.get_legal_moves_bits('white'))
        score = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score, 10)
        board8._black_bitboard = 0x0703012010003C7E
        score = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score, 310)

        score = evaluator.evaluate('black', board8, None, None)
        self.assertEqual(score, -10006)

        # Evaluator_BW
        evaluator = coord.Evaluator_BW()
        board8._black_bitboard = 0x0000002010003C7C
        possibility_b = board8.get_bit_count(board8.get_legal_moves_bits('black'))
        possibility_w = board8.get_bit_count(board8.get_legal_moves_bits('white'))
        score = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score, 2)
        board8._black_bitboard = 0x0703012010003C7E
        score = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score, -2)

        score = evaluator.evaluate('black', board8, None, None)
        self.assertEqual(score, -10006)

        # Evaluator_EcW
        evaluator = coord.Evaluator_EcW()
        board8._black_bitboard = 0x0000002010003C7C
        possibility_b = board8.get_bit_count(board8.get_legal_moves_bits('black'))
        possibility_w = board8.get_bit_count(board8.get_legal_moves_bits('white'))
        score = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score, -16)
        board8._black_bitboard = 0x0703012010003C7E
        score = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score, 0)

        score = evaluator.evaluate('black', board8, None, None)
        self.assertEqual(score, -10006)

        # Evaluator_BWEc
        evaluator = coord.Evaluator_BWEc()
        board8._black_bitboard = 0x0000002010003C7C
        possibility_b = board8.get_bit_count(board8.get_legal_moves_bits('black'))
        possibility_w = board8.get_bit_count(board8.get_legal_moves_bits('white'))
        score = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score, -14)
        board8._black_bitboard = 0x0703012010003C7E
        score = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score, -2)

        score = evaluator.evaluate('black', board8, None, None)
        self.assertEqual(score, -10006)

    def test_evaluator_force_import_error(self):
        import os
        import importlib
        import reversi

        # -------------------------------
        # switch environ and reload module
        os.environ['FORCE_CYTHONMETHODS_IMPORT_ERROR'] = 'RAISE'
        importlib.reload(reversi.cy)
        importlib.reload(reversi.strategies.coordinator.EvaluatorMethods)
        self.assertTrue(reversi.strategies.coordinator.EvaluatorMethods.SLOW_MODE)
        # -------------------------------

        # Evaluator_TPW_Fast
        board8 = BitBoard(8)
        board8.put_disc('black', 3, 2)
        board8.put_disc('white', 2, 2)
        board8.put_disc('black', 2, 3)
        board8.put_disc('white', 4, 2)
        board8.put_disc('black', 1, 1)

        possibility_b = board8.get_bit_count(board8.get_legal_moves_bits('black'))
        possibility_w = board8.get_bit_count(board8.get_legal_moves_bits('white'))

        evaluator = coord.Evaluator_TPW_Fast()
        score = evaluator.evaluate(None, board8, None, None)
        self.assertEqual(score, 10001)

        board8.put_disc('white', 0, 0)

        possibility_b = board8.get_bit_count(board8.get_legal_moves_bits('black'))
        possibility_w = board8.get_bit_count(board8.get_legal_moves_bits('white'))

        score = evaluator.evaluate(None, board8, None, None)
        self.assertEqual(score, -10006)
        score = evaluator.evaluate(None, board8, possibility_b, possibility_w)
        self.assertEqual(score, -17)

        # Evaluator_TPWE_Fast
        board8 = BitBoard(8)
        board8.put_disc('black', 3, 2)
        board8.put_disc('white', 2, 2)
        board8.put_disc('black', 2, 3)
        board8.put_disc('white', 4, 2)
        board8.put_disc('black', 1, 1)

        possibility_b = board8.get_bit_count(board8.get_legal_moves_bits('black'))
        possibility_w = board8.get_bit_count(board8.get_legal_moves_bits('white'))

        evaluator = coord.Evaluator_TPWE_Fast()
        score = evaluator.evaluate(None, board8, None, None)
        self.assertEqual(score, 10001)

        board8.put_disc('white', 0, 0)

        board8._black_bitboard = 0x0000002010003C7E
        possibility_b = board8.get_bit_count(board8.get_legal_moves_bits('black'))
        possibility_w = board8.get_bit_count(board8.get_legal_moves_bits('white'))
        score = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score, -81)

        board8._black_bitboard = 0x0000002010003C7C
        score = evaluator.evaluate('black', board8, possibility_b, possibility_w)
        self.assertEqual(score, -61)

        score = evaluator.evaluate('black', board8, None, None)
        self.assertEqual(score, -10006)

        board4 = BitBoard(4)
        possibility_b = board4.get_bit_count(board4.get_legal_moves_bits('black'))
        possibility_w = board4.get_bit_count(board4.get_legal_moves_bits('white'))
        score = evaluator.evaluate('black', board4, possibility_b, possibility_w)
        self.assertEqual(score, 0)

        # -------------------------------
        # recover environment and reload module
        del os.environ['FORCE_CYTHONMETHODS_IMPORT_ERROR']
        importlib.reload(reversi.cy)
        importlib.reload(reversi.strategies.coordinator.EvaluatorMethods)
        self.assertFalse(reversi.strategies.coordinator.EvaluatorMethods.SLOW_MODE)
        # -------------------------------
