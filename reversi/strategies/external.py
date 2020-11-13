"""
外部コマンド実行用
"""

import subprocess
from subprocess import PIPE, TimeoutExpired
import re
import tkinter as tk

from reversi.strategies.common import AbstractStrategy


TIMEOUT_TIME = 60  # タイムアウト時間(s)


class External(AbstractStrategy):
    """
    外部コマンドを実行する
    """
    def __init__(self, cmd=None, timeouttime=TIMEOUT_TIME):
        self.cmd = cmd
        self.timeouttime = timeouttime

    def next_move(self, color, board):
        """
        次の一手
        """
        color_num = '1' if color == 'black' else '-1'
        board_size = board.size
        board_info = "\n".join([" ".join(row) for row in [[str(col) for col in row] for row in board.get_board_info()]])

        # {手番の色(黒:1、白:-1)}
        # {ボードのサイズ(4～26までの偶数)}
        # {ボードの情報(空:0、黒:1、白:-1)}
        # ex)
        # -1
        # 8
        # 0 0 0 0 0 0 0 0
        # 0 0 0 0 0 0 0 0
        # 0 0 0 1 1 1 0 0
        # 0 0 0 -1 1 0 0 0
        # 0 0 -1 -1 1 -1 0 0
        # 0 0 0 0 1 -1 0 0
        # 0 0 0 0 1 -1 0 0
        # 0 0 0 0 0 0 0 0
        input_data = "\n".join([color_num, str(board_size), board_info])

        # 外部コマンド実行
        out = None
        if self.cmd:
            with subprocess.Popen(self.cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True) as pipe:
                try:
                    out, err = pipe.communicate(input_data, timeout=self.timeouttime)
                except TimeoutExpired:
                    pipe.kill()

                    # タイムアウトした場合は反則負け
                    self.error_message('コマンドがタイムアウトしました。')
                    return (board_size//2-1, board_size//2-1)

            status = pipe.poll()

            # プロセスが正常終了
            if status == 0:
                # 戻り値がある場合
                try:
                    x, y = out.split()
                    # xとyが整数の場合
                    if re.match(r'^\d+$', x) is not None and re.match(r'^\d+$', y) is not None:
                        return (int(x), int(y))
                    else:
                        out = out.rstrip()
                        self.error_message('プログラムからの戻り値が想定外でした(2)。戻り値(' + str(out) + ')')
                except:  # noqa: E722
                    self.error_message('プログラムからの戻り値が想定外でした(1)。戻り値(' + str(out) + ')')
            else:
                self.error_message('プロセスが異常終了しました。終了ステータス(' + str(status) + ')' + '\n(標準エラー出力)\n' + str(err))
        else:
            self.error_message('コマンドが設定されていません。')

        # 戻り値が正しくない場合は反則負け
        return (board_size//2-1, board_size//2-1)

    def error_message(self, message):
        """
        エラーメッセージ
        """
        root = tk.Tk()
        root.title('Error')
        root.minsize(300, 30)
        label = tk.Label(root, text=message)
        label.pack(fill='x', padx='5', pady='5')
        self._mainloop(root)

    def _mainloop(self, root):
        """
        tkinter起動
        """
        root.mainloop()
