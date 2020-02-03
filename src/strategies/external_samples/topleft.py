#!/usr/bin/env python
import sys

def get_message():
    """
    標準入力の読み込み
    """
    lines = sys.stdin.read().split('\n')
    color = int(lines.pop(0))
    size = int(lines.pop(0))
    board = [[int(i) for i in line.split()] for line in lines]

    return (color, size, board)


if __name__ == '__main__':
    # 標準入力を受ける
    color, size, board = get_message()
    print(color, file=sys.stderr)
    print(size, file=sys.stderr)
    print(board, file=sys.stderr)

    # 結果を標準出力
    print('0 0')
