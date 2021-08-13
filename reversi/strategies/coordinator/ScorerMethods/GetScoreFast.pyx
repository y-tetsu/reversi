#cython: language_level=3
"""GetScore
"""

def get_blank_score(board, w1, w2, w3):
    size = board.size
    board_info = board.get_board_info()
    directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    corners = [0, size-1, size*size-8, size*size-1]
    score = 0
    for i in range(size*size):
        x, y = i % size, i // size
        # 自分または相手の石が存在する
        if board_info[x][y]:
            value = 0
            for index, (dx, dy) in enumerate(directions):
                next_x1, next_y1 = x + dx, y + dy
                next_x2, next_y2 = x - dx, y - dy
                if 0 <= next_x1 < size and 0 <= next_y1 < size and 0 <= next_x2 < size and 0 <= next_y2 < size:
                    if not board_info[next_x1][next_y1]:
                        value += w1
                        # 隅に接している場合
                        d = dy * size + dx
                        if i+d in corners:
                            if abs(dx) + abs(dy) == 2:
                                value += w2  # X打ち(チェック方向が斜め)の場合
                            else:
                                for k in range(1, 5):
                                    next_x3, next_y3 = x - k * dx, y - k * dy
                                    if not board_info[next_x3][next_y3]:
                                        value += w3  # 隅の反対の縦横方向に空きマスがある場合
            score += value * board_info[x][y]
    return score
