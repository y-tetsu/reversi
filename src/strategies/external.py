#!/usr/bin/env python
"""
外部コマンド実行用
"""

import sys
sys.path.append('../')

import subprocess
from subprocess import PIPE, TimeoutExpired
import re

from strategies.common import AbstractStrategy


TIMEOUT_TIME = 180  # タイムアウト時間(s)


class External(AbstractStrategy):
    """
    外部コマンドを実行する
    """
    def __init__(self, cmd=None):
        self.cmd = cmd

    def next_move(self, color, board):
        """
        次の一手
        """
        color_num = '0' if color == 'black' else '1'
        size = board.size
        info = "\n".join([" ".join(row) for row in [[str(col) for col in row] for row in board.get_board_info()]])

        # {手番の色}
        # {ボードのサイズ}
        # {ボードの情報}
        # ex)
        # 1
        # 8
        # 0 0 0 0 0 0 0 0
        # 0 0 0 0 0 0 0 0
        # 0 0 0 1 1 1 0 0
        # 0 0 0 -1 1 0 0 0
        # 0 0 -1 -1 1 -1 0 0
        # 0 0 0 0 1 -1 0 0
        # 0 0 0 0 1 -1 0 0
        # 0 0 0 0 0 0 0 0
        input_info = "\n".join([color_num, str(size), info])

        # 外部コマンド実行
        out = None
        if self.cmd:
            with subprocess.Popen(self.cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True) as pipe:
                try:
                    out, err = pipe.communicate(input_info, timeout=TIMEOUT_TIME)
                except TimeoutExpired:
                    pipe.kill()

        # 戻り値がある場合
        if out:
            x, y = out.split()
            # xとyが整数の場合
            if re.match(r'^\d+$', x) is not None and re.match(r'^\d+$', y) is not None:
                return (int(x), int(y))

        # 戻り値が正しくない場合は反則負け
        return (size//2-1, size//2-1)


if __name__ == '__main__':
    import time
    import os
    from board import BitBoard

    bitboard8 = BitBoard()
    bitboard8.put_stone('black', 3, 2)
    bitboard8.put_stone('white', 2, 4)
    bitboard8.put_stone('black', 5, 5)
    bitboard8.put_stone('white', 4, 2)
    bitboard8.put_stone('black', 5, 2)
    bitboard8.put_stone('white', 5, 4)
    bitboard8.put_stone('black', 4, 5)
    bitboard8.put_stone('white', 5, 6)
    bitboard8.put_stone('black', 4, 6)
    print(bitboard8)

    # python実行
    external = External('python .\external_samples\python_sample.py')
    move = external.next_move('white', bitboard8)
    print(move)
