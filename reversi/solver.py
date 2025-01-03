"""Solver
"""

import os
import datetime
import shutil

from reversi import BitBoard, Game, Player, Recorder
from reversi import C as c
from reversi.strategies import Random, _EndGame_


class Solver:
    """ボード解析ツール"""
    def __init__(self, name=None, size=None, first=None, hole=None, ini_black=None, ini_white=None, board=None):
        self.name = name
        self.size = size
        self.first = first
        self.hole = hole
        self.ini_black = ini_black
        self.ini_white = ini_white

        if board is None:
            self.board = BitBoard(size=size, hole=hole, ini_black=ini_black, ini_white=ini_white)
        else:
            self.size = board.size
            self.hole = board._hole_bitboard
            self.ini_black = board._ini_black
            self.ini_white = board._ini_white
            self.board = board

        self._load_board_counts(self.board)

    def _load_board_counts(self, board):
        self.all_squares = board.size * board.size
        self.hole_count = board.get_bit_count(board._hole_bitboard)
        self.ini_count = board.get_bit_count(board._ini_black | board._ini_white)
        self.squares = str(self.all_squares - self.hole_count) + ' / ' + str(self.all_squares)
        self.blanks = self.all_squares - self.hole_count - self.ini_count
        self.perfect_score = self.all_squares - self.hole_count

    def _is_perfect(self):
        return self._is_black_perfect() or self._is_white_perfect()

    def _is_black_perfect(self):
        bb, _, _ = self.board.get_bitboard_info()
        return self.board.get_bit_count(bb) == self.perfect_score

    def _is_white_perfect(self):
        _, wb, _ = self.board.get_bitboard_info()
        return self.board.get_bit_count(wb) == self.perfect_score

    def _get_now_datetime(self):
        t_delta = datetime.timedelta(hours=9)
        JST = datetime.timezone(t_delta, 'JST')
        return datetime.datetime.now(JST)

    def make_perfect_win_txt(self, perfect_win_txt='./perfect_win.txt'):
        if not self._is_perfect():
            return
        with open(perfect_win_txt, 'a') as f:
            f.write('\n')
            f.write('-------------------------------------------\n')
            now = self._get_now_datetime()
            f.write(now.strftime('%Y/%m/%d %H:%M:%S') + '\n')
            f.write('-------------------------------------------\n')
            if self._is_black_perfect():
                f.write('* Black perfect win *\n')
            else:
                f.write('* White perfect win *\n')
            f.write('\n')
            f.write(str(self.board) + '\n')
            f.write("(black) " + str(self.board._black_score) + " - " + str(self.board._white_score) + " (white)\n")
            f.write(str(Recorder(self.board)) + '\n')

    def get_random_match_result(self, matches=10000):
        from reversi import Simulator

        black, white = 'Black', 'White'
        players_info = {black: Random(), white: Random()}
        simulator = Simulator(
                        players_info,
                        first=self.first,
                        board_type='bitboard',
                        board_hole=self.hole,
                        ini_black=self.ini_black,
                        ini_white=self.ini_white,
                        random_opening=0,
                        swap=False,
                        matches=matches,
                        perfect_check=True,
                        progress=False,
                    )
        simulator.start()

        # print result
        random_win_black_rate = "{:3.1f}%".format(simulator.result_ratio[black])
        random_win_white_rate = "{:3.1f}%".format(simulator.result_ratio[white])
        result = "(black) " + random_win_black_rate + " - " + random_win_white_rate + " (white)"
        print("random_" + str(matches) + "_matches :", result)

        # manage perfect text
        perfect_win_txt = simulator.perfect_win_txt
        if os.path.isfile(perfect_win_txt):
            now = self._get_now_datetime()
            dst_txt = 'perfect_win_' + self.name + '_' + now.strftime('%Y%m%d%H%M%S') + '.txt'
            shutil.move(perfect_win_txt, dst_txt)

        return result

    def get_best_match_winner(self):
        black = Player(c.black, 'black', _EndGame_(depth=64))
        white = Player(c.white, 'white', _EndGame_(depth=64))
        self.board = BitBoard(size=self.size, hole=self.hole, ini_black=self.ini_black, ini_white=self.ini_white)
        game = Game(black, white, self.board, color=self.first)
        game.play()
        winlose = 'draw'
        if game.result.winlose == Game.BLACK_WIN:
            winlose = 'black'
        elif game.result.winlose == Game.WHITE_WIN:
            winlose = 'white'
        record = str(Recorder(self.board))
        print('best match winner :', winlose)
        score = '(black) ' + str(game.result.black_num) + ' - ' + str(game.result.white_num) + ' (white)'
        print('            score :', score)
        print('           record :', record)
        return winlose, score, record

    def get_max_winner(self):
        ret = []
        roles = ['black_max', 'white_max']
        for role in roles:
            now = self._get_now_datetime()
            print()
            print(now.strftime('%Y/%m/%d %H:%M:%S'))

            black = Player(c.black, 'black', _EndGame_(depth=64, role=role))
            white = Player(c.white, 'white', _EndGame_(depth=64, role=role))
            self.board = BitBoard(size=self.size, hole=self.hole, ini_black=self.ini_black, ini_white=self.ini_white)
            game = Game(black, white, self.board, color=self.first)

            print()
            print('[' + self.name + ' : ' + role.upper() + ']')
            print(self.board)
            game.play()
            print(self.board)
            score = "(black) " + str(self.board._black_score) + ' - ' + str(self.board._white_score) + " (white)"
            record = str(Recorder(self.board))
            print('score  =', score)
            print('record =', record)
            ret.append(score)
            ret.append(record)

            now = self._get_now_datetime()
            print()
            print(now.strftime('%Y/%m/%d %H:%M:%S'))
        return ret[0], ret[1], ret[2], ret[3]

    def get_shortest_winner(self, limit_depth=12):
        ret = []
        roles = ['black_shortest', 'white_shortest']
        for role in roles:
            now = self._get_now_datetime()
            print()
            print(now.strftime('%Y/%m/%d %H:%M:%S'))

            self.board = BitBoard(size=self.size, hole=self.hole, ini_black=self.ini_black, ini_white=self.ini_white)

            print()
            print('[' + self.name + ' : ' + role.upper() + ']')

            # shotest move check
            depth, max_depth = 0, limit_depth
            move_count, record = '"?"', "?"
            for d in range(1, max_depth + 1):
                moves = self.board.get_legal_moves(self.first)
                _, scores, record = _EndGame_(role=role).get_best_record(self.first, self.board, moves, depth=d)
                if len([s for s in scores.values() if s > 10000]):
                    depth = d
                    break

            if depth:
                move_count = len(record) // 2
                Recorder(self.board).play(record, show_moves=False)
                print('move count =', move_count)
                print('record     =', record)
            else:
                record = "?"
                print('shortest winner check passed. because depth >', max_depth)

            ret.append(move_count)
            ret.append(record)

            now = self._get_now_datetime()
            print()
            print(now.strftime('%Y/%m/%d %H:%M:%S'))
        return ret[0], ret[1], ret[2], ret[3]

    def verify_record(self, record, black_score=None, white_score=None, move_count=None):
        self.board = BitBoard(size=self.size, hole=self.hole, ini_black=self.ini_black, ini_white=self.ini_white)
        recorder = Recorder(self.board)
        is_valid_record = recorder.play(record, show_moves=False)
        black_score_verify = '---'
        white_score_verify = '---'
        move_count_verify = '---'
        print('is_valid_record    :', is_valid_record)
        if is_valid_record:
            if black_score is not None:
                if recorder.board._black_score == black_score:
                    black_score_verify = 'OK'
                else:
                    black_score_verify = 'NG'
                print('black_score_verify :', black_score_verify, recorder.board._black_score, black_score)
            if white_score is not None:
                if recorder.board._white_score == white_score:
                    white_score_verify = 'OK'
                else:
                    white_score_verify = 'NG'
                print('white_score_verify :', white_score_verify, recorder.board._white_score, white_score)
            if move_count is not None:
                if (len(record) // 2) == move_count:
                    move_count_verify = 'OK'
                else:
                    move_count_verify = 'NG'
                print('move_verify        :', move_count_verify, len(record) // 2, move_count)
