import os
import pyximport
pyximport.install()


CYTHON = True


try:
    if 'FORCE_BITBOARDMETHODS_IMPORT_ERROR' in os.environ:
        if os.environ['FORCE_BITBOARDMETHODS_IMPORT_ERROR'] == 'RAISE':
            raise ImportError
    from reversi.cy.BitBoardMethods import get_legal_moves, get_legal_moves_bits, get_bit_count, get_flippable_discs, put_disc, get_board_info, undo, CythonBitBoard  # noqa: E501
    CYTHON = False

except ImportError:
    from reversi.BitBoardMethods.GetLegalMoves import get_legal_moves, get_legal_moves_bits, get_bit_count
    from reversi.BitBoardMethods.GetFlippableDiscs import get_flippable_discs
    from reversi.BitBoardMethods.PutDisc import put_disc
    from reversi.BitBoardMethods.GetBoardInfo import get_board_info
    from reversi.BitBoardMethods.Undo import undo


__all__ = [
    'get_legal_moves',
    'get_legal_moves_bits',
    'get_bit_count',
    'get_flippable_discs',
    'get_board_info',
    'undo',
    'put_disc',
    'CythonBitBoard',
]
