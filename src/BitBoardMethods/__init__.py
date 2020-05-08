#!/usr/bin/env python
import pyximport
pyximport.install()

try:
    from BitBoardMethods.GetLegalMovesFast import get_legal_moves
except ImportError:
    from BitBoardMethods.GetLegalMoves import get_legal_moves

try:
    from BitBoardMethods.GetBoardInfoFast import get_board_info
except ImportError:
    from BitBoardMethods.GetBoardInfo import get_board_info
