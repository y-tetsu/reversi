"""Recorder
"""


class Recorder:
    """
    棋譜
    """
    def __init__(self, board=None):
        self.board = board
        self.record = None
        if board is not None:
            self.record = self.get_record(board)

    def __str__(self):
        return self.record

    def get_record(self, board):
        from reversi import PyListBoard
        if isinstance(board, PyListBoard):
            record = self.get_record_for_listboard(board)
        else:
            record = self.get_record_for_bitboard(board)
        return record

    def get_record_for_listboard(self, board):
        from reversi import Move, UPPER, LOWER
        from reversi import C as c
        record = []
        for i in board.prev:
            case = UPPER if i['color'] == c.black else LOWER
            x, y = i['x'], i['y']
            record += str(Move(x, y, case=case))
        return ''.join(record)

    def get_record_for_bitboard(self, board):
        return self.get_record_by_custom(board.size, board._black_bitboard, board._white_bitboard, board.prev)

    def get_record_by_custom(self, size, last_bb, last_wb, prev):
        from reversi import Move, UPPER, LOWER
        record = []
        for index, (board_b, board_w, score_b, _) in enumerate(prev):
            next_board_b = prev[index+1][0] if index < len(prev) - 1 else last_bb
            next_board_w = prev[index+1][1] if index < len(prev) - 1 else last_wb
            next_score_b = prev[index+1][2] if index < len(prev) - 1 else self.popcount(size, last_bb)
            case = UPPER if next_score_b > score_b else LOWER
            move = Move(*self._get_move_bit(size, board_b, board_w, next_board_b, next_board_w), case=case)
            record.append(str(move))
        return ''.join(record)

    def popcount(self, size, bits):
        count = 0
        mask = 1 << ((size**2)-1)
        for _ in range(size**2):
            if bits & mask:
                count += 1
            mask >>= 1
        return count

    def _get_move_bit(self, size, bb_pre, wb_pre, bb_now, wb_now):
        all_pre = bb_pre | wb_pre
        move = (bb_now & ~all_pre) | (wb_now & ~all_pre)
        mask = 1 << ((size * size) - 1)
        for y in range(size):
            for x in range(size):
                if move & mask:
                    return x, y
                mask >>= 1
        return -1, -1

    def play(self, record=None, board=None, show_moves=True, show_result=True):
        from reversi import BitBoard, Move
        from reversi import C as c
        if record is None:
            record = self.record
        else:
            self.record = record
        if board is None:
            board = self.board
        size, hole, ini_black, ini_white = board.size, board._hole_bitboard, board._ini_black, board._ini_white
        bitboard = BitBoard(size=size, hole=hole, ini_black=ini_black, ini_white=ini_white)
        print(bitboard)
        if not record:
            print('* no record *')
        else:
            if show_moves:
                print(' play :', record)
                print()
        for index in range(0, len(record) - 1, 2):
            str_move = record[index:index+2]
            color = c.black if str_move.isupper() else c.white
            xy_move = Move(str_move)
            if bitboard.put_disc(color, *xy_move):
                if show_moves:
                    print('>>>', str_move)
                    print(bitboard)
            else:
                return False
        if show_result:
            print(bitboard)
        self.board = bitboard
        return True
