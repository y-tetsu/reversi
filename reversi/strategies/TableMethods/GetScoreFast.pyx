#cython: language_level=3
"""Get Score of Table strategy
"""


def get_score(color, table, board):
    """get_score
    """
    return _get_score(color, table, board)


cdef _get_score(color, table, board):
    """_get_score
    """
    sign = 1 if color == 'black' else -1
    board_info = board.get_board_info()
    size = board.size
    score = 0

    for y in range(size):
        for x in range(size):
            score += table[y][x] * board_info[y][x] * sign

    return score
