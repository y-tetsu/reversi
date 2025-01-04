import os
import pyximport
pyximport.install()


IMPORTED = False


try:
    if 'FORCE_CYTHONMETHODS_IMPORT_ERROR' in os.environ:
        if os.environ['FORCE_CYTHONMETHODS_IMPORT_ERROR'] == 'RAISE':
            raise ImportError
    from reversi.cy.ReversiMethods import get_legal_moves, get_legal_moves_bits, get_bit_count, get_flippable_discs, put_disc, get_board_info, undo, CythonBitBoard  # noqa: E501
    IMPORTED = True

except ImportError:
    if 'FORCE_CYTHONMETHODS_IMPORT_ERROR' not in os.environ:
        raise ImportError("failed to import Cython ReversiMethods")


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
