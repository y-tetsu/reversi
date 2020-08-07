"""Get Score of Table strategy
"""


def get_score(table, board):
    """get_score
    """
    board_info = board.get_board_info()
    size = board.size
    score = 0

    for y in range(size):
        for x in range(size):
            score += table[y][x] * board_info[y][x]

    return score
