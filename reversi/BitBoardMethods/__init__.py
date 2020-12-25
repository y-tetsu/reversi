import os
import pyximport
pyximport.install()


SLOW_MODE1 = True
SLOW_MODE2 = True
SLOW_MODE3 = True
SLOW_MODE4 = True
SLOW_MODE5 = True


try:
    if 'FORCE_BITBOARDMETHODS_IMPORT_ERROR' in os.environ:
        if os.environ['FORCE_BITBOARDMETHODS_IMPORT_ERROR'] == 'RAISE':
            raise ImportError

    from reversi.BitBoardMethods.GetLegalMovesFast import get_legal_moves, get_legal_moves_bits, get_bit_count
    SLOW_MODE1 = False
except ImportError:
    from reversi.BitBoardMethods.GetLegalMoves import get_legal_moves, get_legal_moves_bits, get_bit_count

try:
    if 'FORCE_BITBOARDMETHODS_IMPORT_ERROR' in os.environ:
        if os.environ['FORCE_BITBOARDMETHODS_IMPORT_ERROR'] == 'RAISE':
            raise ImportError

    from reversi.BitBoardMethods.GetFlippableDiscsFast import get_flippable_discs
    SLOW_MODE2 = False
except ImportError:
    from reversi.BitBoardMethods.GetFlippableDiscs import get_flippable_discs

try:
    if 'FORCE_BITBOARDMETHODS_IMPORT_ERROR' in os.environ:
        if os.environ['FORCE_BITBOARDMETHODS_IMPORT_ERROR'] == 'RAISE':
            raise ImportError

    from reversi.BitBoardMethods.GetBoardInfoFast import get_board_info
    SLOW_MODE3 = False
except ImportError:
    from reversi.BitBoardMethods.GetBoardInfo import get_board_info

try:
    if 'FORCE_BITBOARDMETHODS_IMPORT_ERROR' in os.environ:
        if os.environ['FORCE_BITBOARDMETHODS_IMPORT_ERROR'] == 'RAISE':
            raise ImportError

    from reversi.BitBoardMethods.UndoFast import undo
    SLOW_MODE4 = False
except ImportError:
    from reversi.BitBoardMethods.Undo import undo

try:
    if 'FORCE_BITBOARDMETHODS_IMPORT_ERROR' in os.environ:
        if os.environ['FORCE_BITBOARDMETHODS_IMPORT_ERROR'] == 'RAISE':
            raise ImportError

    from reversi.BitBoardMethods.PutDiscFast import put_disc
    SLOW_MODE5 = False
except ImportError:
    from reversi.BitBoardMethods.PutDisc import put_disc


__all__ = [
    'get_legal_moves',
    'get_legal_moves_bits',
    'get_bit_count',
    'get_flippable_discs',
    'get_board_info',
    'undo',
    'put_disc',
]
