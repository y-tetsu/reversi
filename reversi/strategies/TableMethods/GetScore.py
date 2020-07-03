"""Get Score of Table strategy
"""


def get_score(color, table, board):
    """get_score
    """
    sign = 1 if color == 'black' else -1
    board_info = board.get_board_info()
    size = board.size
    score = 0

    for y in range(size):
        for x in range(size):
            score += table[y][x] * board_info[y][x] * sign

    return score
