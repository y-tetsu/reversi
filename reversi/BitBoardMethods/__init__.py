#!/usr/bin/env python
import pyximport
pyximport.install()

try:
    from reversi.BitBoardMethods.GetLegalMovesFast import get_legal_moves
except ImportError:
    from reversi.BitBoardMethods.GetLegalMoves import get_legal_moves

try:
    from reversi.BitBoardMethods.GetBoardInfoFast import get_board_info
except ImportError:
    from reversi.BitBoardMethods.GetBoardInfo import get_board_info
