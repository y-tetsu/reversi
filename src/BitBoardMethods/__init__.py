#!/usr/bin/env python
import pyximport
pyximport.install()

try:
    from BitBoardMethods.GetPossiblesFast import get_possibles
except ImportError:
    from BitBoardMethods.GetPossibles import get_possibles

try:
    from BitBoardMethods.GetBoardInfoFast import get_board_info
except ImportError:
    from BitBoardMethods.GetBoardInfo import get_board_info
