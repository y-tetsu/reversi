#!/usr/bin/env python
import pyximport
pyximport.install()

SLOW_MODE1 = True
SLOW_MODE2 = True
SLOW_MODE3 = True

try:
    from reversi.BitBoardMethods.GetLegalMovesFast import get_legal_moves
    SLOW_MODE1 = False
except ImportError:
    from reversi.BitBoardMethods.GetLegalMoves import get_legal_moves

try:
    from reversi.BitBoardMethods.GetBoardInfoFast import get_board_info
    SLOW_MODE2 = False
except ImportError:
    from reversi.BitBoardMethods.GetBoardInfo import get_board_info

try:
    from reversi.BitBoardMethods.UndoFast import undo
    SLOW_MODE3 = False
except ImportError:
    from reversi.BitBoardMethods.Undo import undo
