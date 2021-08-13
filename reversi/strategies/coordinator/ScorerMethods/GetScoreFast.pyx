#cython: language_level=3
"""GetScore
"""

import sys

MAXSIZE64 = 2**63 - 1


def get_blank_score(board, w1, w2, w3):
    return _get_blank_score(board, w1, w2, w3)


cdef inline signed int _get_blank_score(board, signed int w1, signed int w2, signed int w3):
    cdef:
        signed int size = board.size
        signed int size_x_size = size * size
        signed int i, x, y, value, j, dx, dy, next_x1, next_y1, next_x2, next_y2, d, dx_abs, dy_abs, k, next_x3, next_y3
        signed int score = 0
        signed int directions[8][2]
        signed int board_info[26][26]

    directions[0][0], directions[0][1] = -1, -1
    directions[1][0], directions[1][1] = 0, -1
    directions[2][0], directions[2][1] = 1, -1
    directions[3][0], directions[3][1] = -1, 0
    directions[4][0], directions[4][1] = 1, 0
    directions[5][0], directions[5][1] = -1, 1
    directions[6][0], directions[6][1] = 0, 1
    directions[7][0], directions[7][1] = 1, 1

    board_info_tmp = board.get_board_info()
    for y in range(size):
        for x in range(size):
            board_info[x][y] = board_info_tmp[x][y]

    for y in range(size):
        for x in range(size):
            i = y * size + x
            # 自分または相手の石が存在する
            if board_info[x][y]:
                value = 0
                for j in range(8):
                    dx, dy = directions[j][0], directions[j][1]
                    next_x1, next_y1 = x + dx, y + dy
                    next_x2, next_y2 = x - dx, y - dy
                    if 0 <= next_x1 < size and 0 <= next_y1 < size and 0 <= next_x2 < size and 0 <= next_y2 < size:
                        if not board_info[next_x1][next_y1]:
                            value += w1
                            # 隅に接している場合
                            d = dy * size + dx
                            if i+d == 0 or i+d == size-1 or i+d == size_x_size-8 or i+d == size_x_size-1:
                                if dx != 0:
                                    dx_abs = 1
                                if dy != 0:
                                    dy_abs = 1
                                if dx_abs + dy_abs == 2:
                                    value += w2  # X打ち(チェック方向が斜め)の場合
                                else:
                                    for k in range(1, 5):
                                        next_x3, next_y3 = x - k * dx, y - k * dy
                                        if not board_info[next_x3][next_y3]:
                                            value += w3  # 隅の反対の縦横方向に空きマスがある場合
                score += value * board_info[x][y]
    return score
