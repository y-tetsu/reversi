import pyximport
pyximport.install()


SLOW_MODE1 = True
SLOW_MODE2 = True
SLOW_MODE3 = True
SLOW_MODE4 = True


#try:
#    from ..BitBoardMethods.GetLegalMovesFast import get_legal_moves
#    SLOW_MODE1 = False
#except ImportError:
#    from ..BitBoardMethods.GetLegalMoves import get_legal_moves
from ..BitBoardMethods.GetLegalMoves import get_legal_moves

from ..BitBoardMethods.GetFlippableDiscs import get_flippable_discs

try:
    from reversi.BitBoardMethods.GetBoardInfoFast import get_board_info
    SLOW_MODE2 = False
except ImportError:
    from ..BitBoardMethods.GetBoardInfo import get_board_info

#try:
#    from ..BitBoardMethods.UndoFast import undo
#    SLOW_MODE3 = False
#except ImportError:
#    from ..BitBoardMethods.Undo import undo
from ..BitBoardMethods.Undo import undo

#try:
#    from ..BitBoardMethods.PutDiscFast import put_disc
#    SLOW_MODE4 = False
#except ImportError:
#    from ..BitBoardMethods.PutDisc import put_disc
from ..BitBoardMethods.PutDisc import put_disc


__all__ = [
    'get_legal_moves',
    'get_flippable_discs',
    'get_board_info',
    'undo',
    'put_disc',
]
