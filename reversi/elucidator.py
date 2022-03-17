"""Elucidator
"""

from reversi import Recorder

import datetime


class Elucidator:
    """
    解明ツール
    """
    def __init__(self, board, perfect_win_txt='./perfect_win.txt'):
        self.board = board
        self.perfect_score = self.get_perfect_score(board)
        self.perfect_win_txt = perfect_win_txt

    def get_perfect_score(self, board):
        return board.size * board.size - board.get_bit_count(board._hole_bitboard)

    def is_perfect(self):
        return self.is_black_perfect() or self.is_white_perfect()

    def is_black_perfect(self):
        bb, _, _ = self.board.get_bitboard_info()
        return self.board.get_bit_count(bb) == self.perfect_score

    def is_white_perfect(self):
        _, wb, _ = self.board.get_bitboard_info()
        return self.board.get_bit_count(wb) == self.perfect_score

    def make_perfect_win_txt(self):
        if not self.is_perfect():
            return
        with open(self.perfect_win_txt, 'a') as f:
            f.write('\n')
            f.write('-------------------------------------------\n')
            t_delta = datetime.timedelta(hours=9)
            JST = datetime.timezone(t_delta, 'JST')
            now = datetime.datetime.now(JST)
            f.write(now.strftime('%Y/%m/%d %H:%M:%S') + '\n')
            f.write('-------------------------------------------\n')
            if self.is_black_perfect():
                f.write('* Black perfect win *\n')
            else:
                f.write('* White perfect win *\n')
            f.write('\n')
            f.write(str(self.board) + '\n')
            f.write(str(Recorder(self.board)) + '\n')
