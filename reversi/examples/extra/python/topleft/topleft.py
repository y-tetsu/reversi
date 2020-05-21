#!/usr/bin/env python
"""
TopLeft : Place it on the left edge of the top as much as possible
"""

import sys


BLANK, BLACK, WHITE = 0, 1, -1


def get_message():
    """
    Load STDIN
    """
    lines = sys.stdin.read().split('\n')
    color = BLACK if int(lines.pop(0)) == 1 else WHITE
    size = int(lines.pop(0))
    board = [[int(i) for i in line.split()] for line in lines]

    return (color, size, board)


def get_legal_moves(color, size, board):
    """
    Get Legal Moves
    """
    legal_moves = {}

    for y in range(size):
        for x in range(size):
            reversibles = get_reversibles(color, size, board, x, y)

            if reversibles:
                legal_moves[(x, y)] = reversibles

    return legal_moves


def get_reversibles(color, size, board, x, y):
    """
    Get Rversibles
    """
    # (-1,  1) (0,  1) (1,  1)
    # (-1,  0)         (1,  0)
    # (-1, -1) (0, -1) (1, -1)
    directions = [
        (-1,  1), (0,  1), (1,  1),
        (-1,  0),          (1,  0),
        (-1, -1), (0, -1), (1, -1)
    ]
    ret = []

    if in_range(size, x, y) and board[y][x] == BLANK:
        for direction in directions:
            tmp = get_reversibles_in_direction(color, size, board, x, y, direction)

            if tmp:
                ret += tmp

    return ret


def get_reversibles_in_direction(color, size, board, x, y, direction):
    """
    Get Reversibles in Direction
    """
    ret = []
    next_x, next_y = x, y
    dx, dy = direction

    while True:
        next_x, next_y = next_x + dx, next_y + dy

        if in_range(size, next_x, next_y):
            next_value = board[next_y][next_x]

            if next_value != BLANK:
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
    Check x, y range
    """
    if 0 <= x < size and 0 <= y < size:
        return True

    return False


if __name__ == '__main__':
    # Get STDIN
    color, size, board = get_message()
    print(color, file=sys.stderr)
    print(size, file=sys.stderr)
    print(board, file=sys.stderr)

    # Get Legal Moves
    legal_moves = list(get_legal_moves(color, size, board).keys())
    print(legal_moves, file=sys.stderr)

    # Get top left edge
    x, y = legal_moves[0]

    # Output STDOUT
    print(x, y)
