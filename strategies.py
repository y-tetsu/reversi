#!/usr/bin/env python
"""
オセロの戦略
"""

import abc
import re
import random
import time
import itertools

import numpy as np


class AbstractStrategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def next_move(self, color, board):
        pass


class Board8Strategy(AbstractStrategy):
    """
    ボードサイズ8より大きい場合はRandom
    """
    @abc.abstractmethod
    def __init__(self):
        pass

    def next_move(self, color, board):
        """
        次の一手
        """
        if board.size <= 8:
            return self.strategy.next_move(color, board)

        return self.random.next_move(color, board)


class Timer:
    """
    タイマー
    """
    start_time = {}
    limit = {}
    max_elp = 0
    cnt = 0

    @classmethod
    def set_timer(cls, key, limit):
        """
        タイマーセット
        """
        Timer.limit[key] = limit

        def _set_timer(func):
            def wrapper(*args, **kwargs):
                Timer.start_time[key] = time.time()

                ret = func(*args, **kwargs)

                return ret

            return wrapper

        return _set_timer

    @classmethod
    def check_timer(cls, key):
        """
        タイマー経過チェック
        """
        def _check_timer(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs) if time.time() - Timer.start_time[key] < Timer.limit[key] else 0

            return wrapper

        return _check_timer

    @classmethod
    def measure_max_elp(cls, func):
        """
        時間計測
        """
        def wrapper(*args, **kwargs):
            time_s = time.time()

            ret = func(*args, **kwargs)

            time_e = time.time()
            elp = time_e - time_s

            if elp > Timer.max_elp:
                Timer.max_elp = elp

            return ret

        return wrapper

    @classmethod
    def count(cls, func):
        """
        コール回数の記録
        """
        def wrapper(*args, **kwargs):
            Timer.cnt += 1

            ret = func(*args, **kwargs)

            return ret

        return wrapper


class ConsoleUserInput(AbstractStrategy):
    """
    コンソールからのユーザ入力
    """
    def __init__(self):
        self.digit = re.compile(r'^[0-9]+$')

    def next_move(self, color, board):
        """
        次の一手
        """
        possibles = list(board.get_possibles(color).keys())
        select = None

        while True:
            user_in = input('>> ')

            if self._is_digit(user_in):
                select = int(user_in) - 1

                if 0 <= select < len(possibles):
                    break

        return possibles[select]

    def _is_digit(self, string):
        """
        半角数字の判定
        """
        return self.digit.match(string) is not None


class WindowUserInput(AbstractStrategy):
    """
    ウィンドウからのユーザ入力
    """
    def __init__(self, window):
        self.window = window

    def next_move(self, color, board):
        """
        次の一手
        """
        moves = list(board.get_possibles(color).keys())
        self.window.board.selectable_moves(moves)

        while True:
            if self.window.board.event.is_set():
                move = self.window.board.move
                self.window.board.event.clear()

                if move in moves:
                    self.window.board.unselectable_moves(moves)
                    break

            time.sleep(0.01)

        return move


class Random(AbstractStrategy):
    """
    ランダム
    """
    def next_move(self, color, board):
        """
        次の一手
        """
        moves = list(board.get_possibles(color).keys())

        return random.choice(moves)


class Greedy(AbstractStrategy):
    """
    なるべく多くとり、複数ある場合はランダム
    """
    def next_move(self, color, board):
        """
        次の一手
        """
        possibles = board.get_possibles(color)
        max_count = max([len(value) for value in possibles.values()])
        moves = [key for key, value in possibles.items() if len(value) == max_count]

        return random.choice(moves)


class Unselfish(AbstractStrategy):
    """
    Greedyの逆
    """
    def next_move(self, color, board):
        """
        次の一手
        """
        possibles = board.get_possibles(color)
        min_count = min([len(value) for value in possibles.values()])
        moves = [key for key, value in possibles.items() if len(value) == min_count]

        return random.choice(moves)


class SlowStarter(AbstractStrategy):
    """
    15%未満:Unselfish、15%以上:Greedy
    """
    def __init__(self):
        self.unselfish = Unselfish()
        self.greedy = Greedy()

    def next_move(self, color, board):
        """
        次の一手
        """
        squares = board.size**2
        blanks = sum([row.count(0) for row in board.get_board_info()])

        # 序盤
        if (squares-blanks)/squares < 0.15:
            return self.unselfish.next_move(color, board)

        # 序盤以降
        return self.greedy.next_move(color, board)


class Table(AbstractStrategy):
    """
    評価テーブルで手を決める(なるべく少なく取る、角を狙う、角のそばは避ける)
    """
    CORNER, C, A, B, X, O = 50, -20, 0, -1, -25, -5

    def __init__(self, size=8):
        self.set_table(size)

    def set_table(self, size):
        """
        評価テーブル設定
        """
        self.size = size
        table = [[Table.B for _ in range(size)] for _ in range(size)]

        # 中
        for num in range(0, size//2, 2):
            if num != size//2 - 1:
                for y, x in itertools.product((num, size-num-1), repeat=2):
                    table[y][x] = Table.A

        for y in range(1, size//2-1, 2):
            for x in range(1, size//2-1, 2):
                if x == y:
                    for tmp_y, tmp_x in itertools.product((y, size-y-1), (x, size-x-1)):
                        table[tmp_y][tmp_x] = Table.X

        for y in range(1, size//2-2, 2):
            for x in range(y+1, size-y-1):
                for tmp_y, tmp_x in ((y, x), (size-y-1, x)):
                    table[tmp_y][tmp_x] = Table.O
                    table[tmp_x][tmp_y] = Table.O

        # 端
        x_min, y_min, x_max, y_max = 0, 0, size - 1, size - 1

        if size >= 6:
            for y in range(size):
                for x in range(size):
                    if (x == x_min or x == x_max) and (y == y_min or y == y_max):
                        table[y][x] = Table.CORNER

                        x_sign = 1 if x == x_min else -1
                        y_sign = 1 if y == y_min else -1

                        table[y][x+(1*x_sign)] = Table.C
                        table[y][x+(2*x_sign)] = Table.B
                        table[y+(1*y_sign)][x] = Table.C
                        table[y+(2*y_sign)][x] = Table.B

        self.table = np.array(table)

    def get_score(self, color, board):
        """
        評価値を取得する
        """
        sign = 1 if color == 'black' else -1
        board_info = np.array(board.get_board_info())
        score = (board_info * self.table * sign).sum()

        return score

    def next_move(self, color, board):
        """
        次の一手
        """
        if self.size != board.size:
            self.set_table(board.size)

        possibles = board.get_possibles(color)
        max_score = None
        moves = {}

        for move in possibles.keys():
            board.put_stone(color, *move)
            score = self.get_score(color, board)

            if max_score is None or score > max_score:
                max_score = score

            if score not in moves:
                moves[score] = []

            moves[score].append(move)
            board.undo()

        return random.choice(moves[max_score])


class MiniMax(AbstractStrategy):
    """
    MiniMax法で次の手を決める
    """
    def __init__(self, depth=3):
        self.depth = depth

    def next_move(self, color, board):
        """
        次の一手
        """
        next_color = 'white' if color == 'black' else 'black'
        moves, best_score = {}, None

        # 打てる手の中から評価値の最も良い手を選ぶ
        for move in board.get_possibles(color).keys():
            board.put_stone(color, *move)  # 一手打つ

            score = self.get_score(next_color, board, self.depth-1)  # 評価値を取得

            if best_score is None:  # 初回は必ず設定
                best_score = score
            else:
                if color == 'black' and score > best_score:    # 黒の場合最大を選択
                    best_score = score
                elif color == 'white' and score < best_score:  # 白の場合最小を選択
                    best_score = score

            # 次の手の候補を記憶
            if score not in moves:
                moves[score] = []
            moves[score].append(move)

            board.undo()  # 打った手を戻す

        return random.choice(moves[best_score])

    def get_score(self, color, board, depth):
        """
        評価値の取得
        """
        possibles_b = board.get_possibles('black', True)  # 黒の打てる場所
        possibles_w = board.get_possibles('white', True)  # 白の打てる場所
        is_game_end =  True if not possibles_b and not possibles_w else False

        # ゲーム終了 or 最大深さに到達
        if is_game_end or depth <= 0:
            return self.evaluate(board, possibles_b, possibles_w)

        # パスの場合
        possibles = possibles_b if color == 'black' else possibles_w
        next_color = 'white' if color == 'black' else 'black'

        if not possibles:
            return self.get_score(next_color, board, depth)

        # 評価値を算出
        best_score = None

        for move in possibles.keys():
            board.put_stone(color, *move)

            score = self.get_score(next_color, board, depth-1)

            if best_score is None:  # 初回は必ず設定
                best_score = score
            else:
                if color == 'black' and score > best_score:    # 黒の場合最大を選択
                    best_score = score
                elif color == 'white' and score < best_score:  # 白の場合最小を選択
                    best_score = score

            board.undo()

        return best_score

    def evaluate(self, board, possibles_b, possibles_w):
        """
        評価値の算出
        """
        ret = 0

        # 対局終了時
        if not possibles_b and not possibles_w:
            ret = board.score['black'] - board.score['white']

            if ret > 0:    # 黒が勝った
                ret += 1000
            elif ret < 0:  # 白が勝った
                ret -= 1000

            return ret

        # 4隅に重みを掛ける
        board_info = board.get_board_info()
        corner = 0

        for x, y in [(0, 0), (0, board.size-1), (board.size-1, 0), (board.size-1, board.size-1)]:
            corner += board_info[y][x]

        ret += corner * 16

        # 置ける場所の数に重みを掛ける
        black_num = len(list(possibles_b.keys()))
        white_num = len(list(possibles_w.keys()))

        ret += (black_num - white_num) * 2

        return ret


class MiniMax1(Board8Strategy):
    """
    MiniMax法で次の手を決める(1手読み)
    """
    def __init__(self):
        self.strategy = MiniMax(1)
        self.random = Random()


class MiniMax2(Board8Strategy):
    """
    MiniMax法で次の手を決める(2手読み)
    """
    def __init__(self):
        self.strategy = MiniMax(2)
        self.random = Random()


class MiniMax3(Board8Strategy):
    """
    MiniMax法で次の手を決める(3手読み)
    """
    def __init__(self):
        self.strategy = MiniMax(3)
        self.random = Random()


class MiniMax4(Board8Strategy):
    """
    MiniMax法で次の手を決める(4手読み)
    """
    def __init__(self):
        self.strategy = MiniMax(4)
        self.random = Random()


class NegaMax(MiniMax):
    """
    NegaMax法で次の手を決める
    """
    @Timer.set_timer('negamax', 0.3)
    def next_move(self, color, board):
        """
        次の一手
        """
        next_color = 'white' if color == 'black' else 'black'
        moves, max_score = {}, None

        # 打てる手の中から評価値の最も高い手を選ぶ
        for move in board.get_possibles(color).keys():
            board.put_stone(color, *move)  # 一手打つ

            score = -self.get_score(next_color, board, self.depth-1)  # 評価値を取得

            if max_score is None or score > max_score:  # 最大値を選択
                max_score = score

            # 次の手の候補を記憶
            if score not in moves:
                moves[score] = []
            moves[score].append(move)

            board.undo()  # 打った手を戻す

        return random.choice(moves[max_score])

    @Timer.count
    @Timer.check_timer('negamax')
    def get_score(self, color, board, depth):
        """
        評価値の取得
        """
        possibles_b = board.get_possibles('black', True)
        possibles_w = board.get_possibles('white', True)
        is_game_end =  True if not possibles_b and not possibles_w else False

        # ゲーム終了 or 最大深さに到達
        if is_game_end or depth <= 0:
            sign = 1 if color == 'black' else -1
            return self.evaluate(board, possibles_b, possibles_w) * sign

        # パスの場合
        possibles = possibles_b if color == 'black' else possibles_w
        next_color = 'white' if color == 'black' else 'black'

        if not possibles:
            return -self.get_score(next_color, board, depth)

        # 評価値を算出
        max_score = None

        for move in possibles.keys():
            board.put_stone(color, *move)

            score = -self.get_score(next_color, board, depth-1)

            if max_score is None or score > max_score:  # 最大値を選択
                max_score = score

            board.undo()

        return max_score


class NegaMax1(Board8Strategy):
    """
    NegaMax法で次の手を決める(1手読み)
    """
    def __init__(self):
        self.strategy = NegaMax(1)
        self.random = Random()


class NegaMax2(Board8Strategy):
    """
    NegaMax法で次の手を決める(2手読み)
    """
    def __init__(self):
        self.strategy = NegaMax(2)
        self.random = Random()


class NegaMax3(Board8Strategy):
    """
    NegaMax法で次の手を決める(3手読み)
    """
    def __init__(self):
        self.strategy = NegaMax(3)
        self.random = Random()


class NegaMax4(Board8Strategy):
    """
    NegaMax法で次の手を決める(4手読み)
    """
    def __init__(self):
        self.strategy = NegaMax(4)
        self.random = Random()


class AlphaBeta(MiniMax):
    """
    AlphaBeta法で次の手を決める
    """
    MIN = -1000000

    @Timer.measure_max_elp
    @Timer.set_timer('alphabeta', 0.3)
    def next_move(self, color, board):
        """
        次の一手
        """
        next_color = 'white' if color == 'black' else 'black'
        moves, alpha, beta = {}, AlphaBeta.MIN, -AlphaBeta.MIN

        # 打てる手の中から評価値の最も高い手を選ぶ
        for move in board.get_possibles(color).keys():
            board.put_stone(color, *move)  # 一手打つ

            #---#
            #print(self.depth, color, move)
            #print(board)
            #---#

            score = -self.get_score(next_color, board, -beta, -alpha, self.depth-1)  # 評価値を取得
            alpha = max(alpha, score)

            #---#
            #print('score1', score, self.depth, color, move, 'alpha =', alpha, 'beta =', beta)
            #---#

            # 次の手の候補を記憶
            if score not in moves:
                moves[score] = []
            moves[score].append(move)

            board.undo()  # 打った手を戻す

        return moves[alpha][0]

    @Timer.count
    @Timer.check_timer('alphabeta')
    def get_score(self, color, board, alpha, beta, depth):
        """
        評価値の取得
        """
        possibles_b = board.get_possibles('black', True)
        possibles_w = board.get_possibles('white', True)
        is_game_end =  True if not possibles_b and not possibles_w else False

        # ゲーム終了 or 最大深さに到達
        if is_game_end or depth <= 0:
            sign = 1 if color == 'black' else -1
            return self.evaluate(board, possibles_b, possibles_w) * sign

        # パスの場合
        possibles = possibles_b if color == 'black' else possibles_w
        next_color = 'white' if color == 'black' else 'black'

        if not possibles:
            return -self.get_score(next_color, board, -beta, -alpha, depth)

        # 評価値を算出
        for move in possibles.keys():
            board.put_stone(color, *move)

            #---#
            #print(depth, color, move)
            #print(board)
            #---#

            score = -self.get_score(next_color, board, -beta, -alpha, depth-1)
            alpha = max(alpha, score)

            board.undo()

            #---#
            #print('score2', score, depth, color, move, 'alpha =', alpha, 'beta =', beta)
            #---#

            if alpha >= beta:
                break

        return alpha


class AlphaBeta1(Board8Strategy):
    """
    AlphaBeta法で次の手を決める(1手読み)
    """
    def __init__(self):
        self.strategy = AlphaBeta(1)
        self.random = Random()


class AlphaBeta2(Board8Strategy):
    """
    AlphaBeta法で次の手を決める(2手読み)
    """
    def __init__(self):
        self.strategy = AlphaBeta(2)
        self.random = Random()


class AlphaBeta3(Board8Strategy):
    """
    AlphaBeta法で次の手を決める(3手読み)
    """
    def __init__(self):
        self.strategy = AlphaBeta(3)
        self.random = Random()


class AlphaBeta4(Board8Strategy):
    """
    AlphaBeta法で次の手を決める(4手読み)
    """
    def __init__(self):
        self.strategy = AlphaBeta(4)
        self.random = Random()


if __name__ == '__main__':
    def input(string):
        print(string + '1')
        return '1'

    from board import Board

    board = Board()
    print(board)
    console_user_input = ConsoleUserInput()

    possibles = board.get_possibles('black')

    for index, value in enumerate(possibles, 1):
        coordinate = (chr(value[0] + 97), str(value[1] + 1))
        print(f'{index:2d}:', coordinate)

    print('User', console_user_input.next_move('black', board))

    random_player = Random()
    print('Random', random_player.next_move('black', board))

    from board import Board
    from player import Player

    board4x4 = Board(4)
    print(board4x4)

    p1 = Player('black', 'Random', Random())
    p2 = Player('white', 'SlowStarter', SlowStarter())

    while True:
        cnt = 0

        for player in [p1, p2]:
            if board4x4.get_possibles(player.color):
                print(player, 'の番です')
                player.put_stone(board4x4)
                move = '(' + chr(player.move[0] + 97) + ', ' + str(player.move[1] + 1) + ')'
                print(move + 'に置きました\n')
                print(board4x4)
                cnt += 1

        if not cnt:
            print('\n終了')
            break

    table4 = Table(4)
    table4_ret = [
        [Table.A, Table.B, Table.B, Table.A],
        [Table.B, Table.B, Table.B, Table.B],
        [Table.B, Table.B, Table.B, Table.B],
        [Table.A, Table.B, Table.B, Table.A],
    ]
    assert (table4.table == np.array(table4_ret)).all()

    table8 = Table(8)
    table8_ret = [
        [Table.CORNER, Table.C, Table.B, Table.B, Table.B, Table.B, Table.C, Table.CORNER],
        [Table.C, Table.X, Table.O, Table.O, Table.O, Table.O, Table.X, Table.C],
        [Table.B, Table.O, Table.A, Table.B, Table.B, Table.A, Table.O, Table.B],
        [Table.B, Table.O, Table.B, Table.B, Table.B, Table.B, Table.O, Table.B],
        [Table.B, Table.O, Table.B, Table.B, Table.B, Table.B, Table.O, Table.B],
        [Table.B, Table.O, Table.A, Table.B, Table.B, Table.A, Table.O, Table.B],
        [Table.C, Table.X, Table.O, Table.O, Table.O, Table.O, Table.X, Table.C],
        [Table.CORNER, Table.C, Table.B, Table.B, Table.B, Table.B, Table.C, Table.CORNER],
    ]
    assert (table8.table == np.array(table8_ret)).all()

    table16 = Table(16)
    table16_ret = [
        [Table.CORNER, Table.C, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.C, Table.CORNER],
        [Table.C, Table.X, Table.O, Table.O, Table.O, Table.O, Table.O, Table.O, Table.O, Table.O, Table.O, Table.O, Table.O, Table.O, Table.X, Table.C],
        [Table.B, Table.O, Table.A, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.A, Table.O, Table.B],
        [Table.B, Table.O, Table.B, Table.X, Table.O, Table.O, Table.O, Table.O, Table.O, Table.O, Table.O, Table.O, Table.X, Table.B, Table.O, Table.B],
        [Table.B, Table.O, Table.B, Table.O, Table.A, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.A, Table.O, Table.B, Table.O, Table.B],
        [Table.B, Table.O, Table.B, Table.O, Table.B, Table.X, Table.O, Table.O, Table.O, Table.O, Table.X, Table.B, Table.O, Table.B, Table.O, Table.B],
        [Table.B, Table.O, Table.B, Table.O, Table.B, Table.O, Table.A, Table.B, Table.B, Table.A, Table.O, Table.B, Table.O, Table.B, Table.O, Table.B],
        [Table.B, Table.O, Table.B, Table.O, Table.B, Table.O, Table.B, Table.B, Table.B, Table.B, Table.O, Table.B, Table.O, Table.B, Table.O, Table.B],
        [Table.B, Table.O, Table.B, Table.O, Table.B, Table.O, Table.B, Table.B, Table.B, Table.B, Table.O, Table.B, Table.O, Table.B, Table.O, Table.B],
        [Table.B, Table.O, Table.B, Table.O, Table.B, Table.O, Table.A, Table.B, Table.B, Table.A, Table.O, Table.B, Table.O, Table.B, Table.O, Table.B],
        [Table.B, Table.O, Table.B, Table.O, Table.B, Table.X, Table.O, Table.O, Table.O, Table.O, Table.X, Table.B, Table.O, Table.B, Table.O, Table.B],
        [Table.B, Table.O, Table.B, Table.O, Table.A, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.A, Table.O, Table.B, Table.O, Table.B],
        [Table.B, Table.O, Table.B, Table.X, Table.O, Table.O, Table.O, Table.O, Table.O, Table.O, Table.O, Table.O, Table.X, Table.B, Table.O, Table.B],
        [Table.B, Table.O, Table.A, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.A, Table.O, Table.B],
        [Table.C, Table.X, Table.O, Table.O, Table.O, Table.O, Table.O, Table.O, Table.O, Table.O, Table.O, Table.O, Table.O, Table.O, Table.X, Table.C],
        [Table.CORNER, Table.C, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.B, Table.C, Table.CORNER],
    ]
    assert (table16.table == np.array(table16_ret)).all()

    board8 = Board(8)
    board8.put_stone('black', 3, 2)
    board8.put_stone('white', 2, 2)
    board8.put_stone('black', 2, 3)
    board8.put_stone('white', 4, 2)
    board8.put_stone('black', 1, 1)
    board8.put_stone('white', 0, 0)
    print(board8)
    for row in table8.table:
        print(row)
    print('black score', table8.get_score('black', board8))
    print('white score', table8.get_score('white', board8))
    assert table8.get_score('black', board8) == -22
    assert table8.get_score('white', board8) == 22
    print('next black', table8.next_move('black', board8))
    print('next white', table8.next_move('white', board8))
    assert table8.next_move('black', board8) == (5, 2)
    assert table8.next_move('white', board8) == (2, 5)

    print("pre", table8.table)
    table8.next_move('black', Board(4))
    print("aft", table8.table)
    assert (table8.table == np.array(table4_ret)).all

    # MiniMax
    print('--- Test For MiniMax Strategy ---')
    board8 = Board(8)
    minimax = MiniMax()
    assert minimax.depth == 3
    print(board8)
    b = board8.get_possibles('black', True)
    w = board8.get_possibles('white', True)
    assert minimax.evaluate(board8, b, w) == 0

    board8.put_stone('black', 3, 2)
    board8.put_stone('white', 2, 4)
    print(board8)
    b = board8.get_possibles('black', True)
    w = board8.get_possibles('white', True)
    assert minimax.evaluate(board8, b, w) == 2

    board8.put_stone('black', 1, 5)
    board8.put_stone('white', 1, 4)
    board8.put_stone('black', 2, 5)
    board8.put_stone('white', 1, 6)
    board8.put_stone('black', 0, 7)
    print(board8)
    b = board8.get_possibles('black', True)
    w = board8.get_possibles('white', True)
    assert minimax.evaluate(board8, b, w) == 22

    board8.put_stone('black', 1, 3)
    board8.put_stone('black', 2, 3)
    board8.put_stone('black', 4, 5)
    print(board8)
    b = board8.get_possibles('black', True)
    w = board8.get_possibles('white', True)
    assert minimax.evaluate(board8, b, w) == 1014

    from board import BitBoard
    print('- bitboard -')
    bitboard8 = BitBoard(8)
    bitboard8.put_stone('black', 3, 2)
    print(bitboard8)
    assert minimax.get_score('white', bitboard8, 2) == 6
    assert minimax.get_score('white', bitboard8, 3) == -2

    print(bitboard8)
    assert minimax.next_move('white', bitboard8) == (2, 4)
    bitboard8.put_stone('white', 2, 4)
    bitboard8.put_stone('black', 5, 5)
    bitboard8.put_stone('white', 4, 2)
    bitboard8.put_stone('black', 5, 2)
    bitboard8.put_stone('white', 5, 4)
    print(bitboard8)
    assert minimax.next_move('black', bitboard8) == (2, 2)

    # NegaMax
    print('--- Test For NegaMax Strategy ---')
    board8 = Board(8)
    negamax = NegaMax()
    assert negamax.depth == 3
    print(board8)
    b = board8.get_possibles('black', True)
    w = board8.get_possibles('white', True)
    assert negamax.evaluate(board8, b, w) == 0

    board8.put_stone('black', 3, 2)
    board8.put_stone('white', 2, 4)
    print(board8)
    b = board8.get_possibles('black', True)
    w = board8.get_possibles('white', True)
    assert negamax.evaluate(board8, b, w) == 2

    board8.put_stone('black', 1, 5)
    board8.put_stone('white', 1, 4)
    board8.put_stone('black', 2, 5)
    board8.put_stone('white', 1, 6)
    board8.put_stone('black', 0, 7)
    print(board8)
    b = board8.get_possibles('black', True)
    w = board8.get_possibles('white', True)
    assert negamax.evaluate(board8, b, w) == 22

    board8.put_stone('black', 1, 3)
    board8.put_stone('black', 2, 3)
    board8.put_stone('black', 4, 5)
    print(board8)
    b = board8.get_possibles('black', True)
    w = board8.get_possibles('white', True)
    assert negamax.evaluate(board8, b, w) == 1014

    from board import BitBoard
    print('- bitboard -')
    bitboard8 = BitBoard(8)
    bitboard8.put_stone('black', 3, 2)

    Timer.cnt = 0
    Timer.start_time['negamax'] = time.time()
    assert negamax.get_score('white', bitboard8, 2) == -6
    assert Timer.cnt == 18

    Timer.cnt = 0
    Timer.start_time['negamax'] = time.time()
    assert negamax.get_score('white', bitboard8, 3) == 2
    assert Timer.cnt == 79

    Timer.cnt = 0
    Timer.start_time['negamax'] = time.time()
    assert negamax.get_score('white', bitboard8, 4) == -4
    assert Timer.cnt == 428

    Timer.cnt = 0
    Timer.limit['negamax'] = 1
    Timer.start_time['negamax'] = time.time()
    assert negamax.get_score('white', bitboard8, 5) == 2
    assert Timer.cnt == 2478

    Timer.cnt = 0
    Timer.limit['negamax'] = 5
    Timer.start_time['negamax'] = time.time()
    assert negamax.get_score('white', bitboard8, 6) == -4
    assert Timer.cnt == 16251

    print(bitboard8)
    assert negamax.next_move('white', bitboard8) == (2, 4)

    bitboard8.put_stone('white', 2, 4)
    bitboard8.put_stone('black', 5, 5)
    bitboard8.put_stone('white', 4, 2)
    bitboard8.put_stone('black', 5, 2)
    bitboard8.put_stone('white', 5, 4)
    print(bitboard8)

    Timer.cnt = 0
    Timer.start_time['negamax'] = time.time()
    assert negamax.next_move('black', bitboard8) == (2, 2)
    assert Timer.cnt == 575

    Timer.cnt = 0
    negamax.depth = 2
    Timer.start_time['negamax'] = time.time()
    assert negamax.next_move('black', bitboard8) == (2, 2)
    assert Timer.cnt == 70

    # AlphaBeta
    print('--- Test For AlphaBeta Strategy ---')
    board8 = Board(8)
    alphabeta = AlphaBeta()
    assert alphabeta.depth == 3
    print(board8)
    b = board8.get_possibles('black', True)
    w = board8.get_possibles('white', True)
    assert alphabeta.evaluate(board8, b, w) == 0

    board8.put_stone('black', 3, 2)
    board8.put_stone('white', 2, 4)
    print(board8)
    b = board8.get_possibles('black', True)
    w = board8.get_possibles('white', True)
    assert alphabeta.evaluate(board8, b, w) == 2

    board8.put_stone('black', 1, 5)
    board8.put_stone('white', 1, 4)
    board8.put_stone('black', 2, 5)
    board8.put_stone('white', 1, 6)
    board8.put_stone('black', 0, 7)
    print(board8)
    b = board8.get_possibles('black', True)
    w = board8.get_possibles('white', True)
    assert alphabeta.evaluate(board8, b, w) == 22

    board8.put_stone('black', 1, 3)
    board8.put_stone('black', 2, 3)
    board8.put_stone('black', 4, 5)
    print(board8)
    b = board8.get_possibles('black', True)
    w = board8.get_possibles('white', True)
    assert alphabeta.evaluate(board8, b, w) == 1014

    from board import BitBoard
    print('- bitboard -')
    bitboard8 = BitBoard(8)
    bitboard8.put_stone('black', 3, 2)

    Timer.cnt = 0
    Timer.start_time['alphabeta'] = time.time()
    assert alphabeta.get_score('white', bitboard8, AlphaBeta.MIN, -AlphaBeta.MIN, 2) == -6
    assert Timer.cnt == 16

    Timer.cnt = 0
    Timer.start_time['alphabeta'] = time.time()
    assert alphabeta.get_score('white', bitboard8, AlphaBeta.MIN, -AlphaBeta.MIN, 3) == 2
    assert Timer.cnt == 58

    Timer.cnt = 0
    Timer.start_time['alphabeta'] = time.time()
    assert alphabeta.get_score('white', bitboard8, AlphaBeta.MIN, -AlphaBeta.MIN, 4) == -4
    assert Timer.cnt == 226

    Timer.cnt = 0
    Timer.limit['alphabeta'] = 1
    Timer.start_time['alphabeta'] = time.time()
    assert alphabeta.get_score('white', bitboard8, AlphaBeta.MIN, -AlphaBeta.MIN, 5) == 2
    assert Timer.cnt == 617

    Timer.cnt = 0
    Timer.limit['alphabeta'] = 3
    Timer.start_time['alphabeta'] = time.time()
    assert alphabeta.get_score('white', bitboard8, AlphaBeta.MIN, -AlphaBeta.MIN, 6) == -4
    assert Timer.cnt == 1865

    print(bitboard8)
    assert alphabeta.next_move('white', bitboard8) == (2, 4)

    print('* black check')
    bitboard8.put_stone('white', 2, 4)
    bitboard8.put_stone('black', 5, 5)
    bitboard8.put_stone('white', 4, 2)
    bitboard8.put_stone('black', 5, 2)
    bitboard8.put_stone('white', 5, 4)
    print(bitboard8)

    Timer.cnt = 0
    Timer.start_time['alphabeta'] = time.time()
    assert alphabeta.next_move('black', bitboard8) == (2, 2)
    assert Timer.cnt == 170

    Timer.cnt = 0
    alphabeta.depth = 2
    Timer.start_time['alphabeta'] = time.time()
    assert alphabeta.next_move('black', bitboard8) == (2, 2)
    assert Timer.cnt == 29
