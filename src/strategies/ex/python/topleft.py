#!/usr/bin/env python
"""
なるべく上の方の左端に置く
"""

import sys


BLANK, BLACK, WHITE = 0, 1, -1


def get_message():
    """
    標準入力の読み込み
    """
    lines = sys.stdin.read().split('\n')
    color = BLACK if int(lines.pop(0)) == 1 else WHITE
    size = int(lines.pop(0))
    board = [[int(i) for i in line.split()] for line in lines]

    return (color, size, board)


def get_possibles(color, size, board):
    """
    石が置ける場所をすべて返す
    """
    possibles = {}

    for y in range(size):
        for x in range(size):
            reversibles = get_reversibles(color, size, board, x, y)

            if reversibles:
                possibles[(x, y)] = reversibles

    return possibles


def get_reversibles(color, size, board, x, y):
    """
    指定座標のひっくり返せる石の場所をすべて返す
    """
    directions = [
        (1, 0), (1, 1), (0, 1), (-1, 1),
        (-1, 0), (-1, -1), (0, -1), (1, -1)
    ]
    ret = []

    # 指定座標が範囲内 かつ 石が置いていない
    if in_range(size, x, y) and board[y][x] == BLANK:
        # 8方向をチェック
        for direction in directions:
            tmp = get_reversibles_in_direction(color, size, board, x, y, direction)

            if tmp:
                ret += tmp

    return ret


def get_reversibles_in_direction(color, size, board, x, y, direction):
    """
    指定座標から指定方向に向けてひっくり返せる石の場所を返す
    """
    ret = []
    next_x, next_y = x, y
    dx, dy = direction

    while True:
        next_x, next_y = next_x + dx, next_y + dy

        # 座標が範囲内
        if in_range(size, next_x, next_y):
            next_value = board[next_y][next_x]

            # 石が置いていない
            if next_value != BLANK:
                # 置いた石と同じ色が見つかった場合
                if next_value == color:
                    return ret

                ret += [(next_x, next_y)]
            else:
                break
        else:
            break

    return []


def in_range(size, x, y):
    """
    座標がボードの範囲内かどうかを返す
    """
    if 0 <= x < size and 0 <= y < size:
        return True

    return False


if __name__ == '__main__':
    # 標準入力を受ける
    color, size, board = get_message()
    print(color, file=sys.stderr)
    print(size, file=sys.stderr)
    print(board, file=sys.stderr)

    # 置ける場所を取得
    possibles = list(get_possibles(color, size, board).keys())

    # 一番上の左端を取得
    x, y = possibles[0]

    # 結果を標準出力
    print(x, y)
