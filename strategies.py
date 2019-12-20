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

from timer import Timer
from measure import Measure


CPU_TIME = 0.5  # CPUの持ち時間(s)


class AbstractStrategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def next_move(self, color, board):
        pass


    def next_move(self, color, board):
        """
        次の一手
        """
        return self.strategy.next_move(color, board)


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
    def __init__(self, size=8, corner=50, c=-20, a=0, b=-1, x=-25, o=-5):
        self._CORNER = corner
        self._C = c
        self._A = a
        self._B = b
        self._X = x
        self._O = o
        self.set_table(size)

    def set_table(self, size):
        """
        評価テーブル設定
        """
        self.size = size
        table = [[self._B for _ in range(size)] for _ in range(size)]

        # 中
        for num in range(0, size//2, 2):
            if num != size//2 - 1:
                for y, x in itertools.product((num, size-num-1), repeat=2):
                    table[y][x] = self._A

        for y in range(1, size//2-1, 2):
            for x in range(1, size//2-1, 2):
                if x == y:
                    for tmp_y, tmp_x in itertools.product((y, size-y-1), (x, size-x-1)):
                        table[tmp_y][tmp_x] = self._X

        for y in range(1, size//2-2, 2):
            for x in range(y+1, size-y-1):
                for tmp_y, tmp_x in ((y, x), (size-y-1, x)):
                    table[tmp_y][tmp_x] = self._O
                    table[tmp_x][tmp_y] = self._O

        # 端
        x_min, y_min, x_max, y_max = 0, 0, size - 1, size - 1

        if size >= 6:
            for y in range(size):
                for x in range(size):
                    if (x == x_min or x == x_max) and (y == y_min or y == y_max):
                        table[y][x] = self._CORNER

                        x_sign = 1 if x == x_min else -1
                        y_sign = 1 if y == y_min else -1

                        table[y][x+(1*x_sign)] = self._C
                        table[y][x+(2*x_sign)] = self._B
                        table[y+(1*y_sign)][x] = self._C
                        table[y+(2*y_sign)][x] = self._B

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


class MinMax(AbstractStrategy):
    """
    MinMax法で次の手を決める
    """
    def __init__(self, depth=3, w1=10000, w2=16, w3=2, min_value=-10000000, max_value=10000000):
        self._W1 = w1
        self._W2 = w2
        self._W3 = w3
        self._MIN = min_value
        self._MAX = max_value
        self.depth = depth

    @Measure.time
    def next_move(self, color, board):
        """
        次の一手
        """
        next_color = 'white' if color == 'black' else 'black'
        next_moves = {}
        best_score = self._MIN if color == 'black' else self._MAX

        # 打てる手の中から評価値の最も良い手を選ぶ
        for move in board.get_possibles(color).keys():
            board.put_stone(color, *move)                            # 一手打つ
            score = self.get_score(next_color, board, self.depth-1)  # 評価値を取得
            board.undo()                                             # 打った手を戻す

            # ベストスコア取得
            best_score = max(best_score, score) if color == 'black' else min(best_score, score)

            # 次の手の候補を記憶
            if score not in next_moves:
                next_moves[score] = []
            next_moves[score].append(move)

        return random.choice(next_moves[best_score])  # 複数候補がある場合はランダムに選ぶ

    def get_score(self, color, board, depth):
        """
        評価値の取得
        """
        # ゲーム終了 or 最大深さに到達
        possibles_b = board.get_possibles('black', True)  # 黒の打てる場所
        possibles_w = board.get_possibles('white', True)  # 白の打てる場所
        is_game_end =  True if not possibles_b and not possibles_w else False

        if is_game_end or depth <= 0:
            return self.evaluate(board, possibles_b, possibles_w)

        # パスの場合
        possibles = possibles_b if color == 'black' else possibles_w
        next_color = 'white' if color == 'black' else 'black'

        if not possibles:
            return self.get_score(next_color, board, depth)

        # 評価値を算出
        best_score = self._MIN if color == 'black' else self._MAX

        for move in possibles.keys():
            board.put_stone(color, *move)
            score = self.get_score(next_color, board, depth-1)
            board.undo()

            # ベストスコア取得
            best_score = max(best_score, score) if color == 'black' else min(best_score, score)

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
                ret += self._W1
            elif ret < 0:  # 白が勝った
                ret -= self._W1

            return ret

        # 4隅に重みを掛ける
        board_info = board.get_board_info()
        corner = 0

        for x, y in [(0, 0), (0, board.size-1), (board.size-1, 0), (board.size-1, board.size-1)]:
            corner += board_info[y][x]

        ret += corner * self._W2

        # 置ける場所の数に重みを掛ける
        black_num = len(list(possibles_b.keys()))
        white_num = len(list(possibles_w.keys()))

        ret += (black_num - white_num) * self._W3

        return ret


class MinMax1(MinMax):
    """
    MinMax法で次の手を決める(1手読み)
    """
    def __init__(self, depth=1):
        super().__init__(depth)


class MinMax2(MinMax):
    """
    MinMax法で次の手を決める(2手読み)
    """
    def __init__(self, depth=2):
        super().__init__(depth)


class MinMax3(MinMax):
    """
    MinMax法で次の手を決める(3手読み)
    """
    def __init__(self, depth=3):
        super().__init__(depth)


class MinMax4(MinMax):
    """
    MinMax法で次の手を決める(4手読み)
    """
    def __init__(self, depth=4):
        super().__init__(depth)


class NegaMax(MinMax):
    """
    NegaMax法で次の手を決める
    """
    @Measure.time
    @Timer.start(CPU_TIME)
    def next_move(self, color, board):
        """
        次の一手
        """
        next_color = 'white' if color == 'black' else 'black'
        moves, max_score = {}, self._MIN

        # 打てる手の中から評価値の最も高い手を選ぶ
        for move in board.get_possibles(color).keys():
            board.put_stone(color, *move)                             # 一手打つ
            score = -self.get_score(next_color, board, self.depth-1)  # 評価値を取得
            board.undo()                                              # 打った手を戻す

            if Timer.is_timeout(self):      # タイムアウト発生時
                if max_score not in moves:  # 候補がない場合は現在の手を返す
                    return move
                break
            else:
                max_score = max(max_score, score)  # 最大値を選択
                if score not in moves:             # 次の候補を記憶
                    moves[score] = []
                moves[score].append(move)

        return random.choice(moves[max_score])  # 複数候補がある場合はランダムに選ぶ

    @Measure.countup
    @Timer.timeout
    def get_score(self, color, board, depth):
        """
        評価値の取得
        """
        # ゲーム終了 or 最大深さに到達
        possibles_b = board.get_possibles('black', True)
        possibles_w = board.get_possibles('white', True)
        is_game_end =  True if not possibles_b and not possibles_w else False

        if is_game_end or depth <= 0:
            sign = 1 if color == 'black' else -1
            return self.evaluate(board, possibles_b, possibles_w) * sign

        # パスの場合
        possibles = possibles_b if color == 'black' else possibles_w
        next_color = 'white' if color == 'black' else 'black'

        if not possibles:
            return -self.get_score(next_color, board, depth)

        # 評価値を算出
        max_score = self._MIN

        for move in possibles.keys():
            board.put_stone(color, *move)
            score = -self.get_score(next_color, board, depth-1)
            board.undo()

            if Timer.is_timeout(self):
                break
            else:
                max_score = max(max_score, score)  # 最大値を選択

        return max_score


class NegaMax1(NegaMax):
    """
    NegaMax法で次の手を決める(1手読み)
    """
    def __init__(self, depth=1):
        super().__init__(depth)


class NegaMax2(NegaMax):
    """
    NegaMax法で次の手を決める(2手読み)
    """
    def __init__(self, depth=2):
        super().__init__(depth)


class NegaMax3(NegaMax):
    """
    NegaMax法で次の手を決める(3手読み)
    """
    def __init__(self, depth=3):
        super().__init__(depth)


class NegaMax4(NegaMax):
    """
    NegaMax法で次の手を決める(4手読み)
    """
    def __init__(self, depth=4):
        super().__init__(depth)


class AlphaBeta(MinMax):
    """
    AlphaBeta法で次の手を決める
    """
    @Measure.time
    @Timer.start(CPU_TIME)
    def next_move(self, color, board):
        """
        次の一手
        """
        next_color = 'white' if color == 'black' else 'black'
        best_move, alpha, beta = None, self._MIN, self._MAX

        # 打てる手の中から評価値の最も高い手を選ぶ
        for move in board.get_possibles(color).keys():
            board.put_stone(color, *move)                                            # 一手打つ
            score = -self.get_score(next_color, board, -beta, -alpha, self.depth-1)  # 評価値を取得
            board.undo()                                                             # 打った手を戻す

            if Timer.is_timeout(self):
                best_move = move if best_move is None else best_move
                break
            else:
                if score > alpha:  # 最善手を更新
                    alpha = score
                    best_move = move

        return best_move

    @Measure.countup
    @Timer.timeout
    def get_score(self, color, board, alpha, beta, depth):
        """
        評価値の取得
        """
        # ゲーム終了 or 最大深さに到達
        possibles_b = board.get_possibles('black', True)
        possibles_w = board.get_possibles('white', True)
        is_game_end =  True if not possibles_b and not possibles_w else False

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
            score = -self.get_score(next_color, board, -beta, -alpha, depth-1)
            board.undo()

            if Timer.is_timeout(self):
                break
            else:
                alpha = max(alpha, score)  # 最大値を選択
                if alpha >= beta:  # 枝刈り
                    break

        return alpha


class AlphaBeta1(AlphaBeta):
    """
    AlphaBeta法で次の手を決める(1手読み)
    """
    def __init__(self, depth=1):
        super().__init__(depth)


class AlphaBeta2(AlphaBeta):
    """
    AlphaBeta法で次の手を決める(2手読み)
    """
    def __init__(self, depth=2):
        super().__init__(depth)


class AlphaBeta3(AlphaBeta):
    """
    AlphaBeta法で次の手を決める(3手読み)
    """
    def __init__(self, depth=3):
        super().__init__(depth)


class AlphaBeta4(AlphaBeta):
    """
    AlphaBeta法で次の手を決める(4手読み)
    """
    def __init__(self, depth=4):
        super().__init__(depth)


class AlphaBeta5(AlphaBeta):
    """
    AlphaBeta法で次の手を決める(5手読み)
    """
    def __init__(self, depth=5):
        super().__init__(depth)


class AlphaBetaT(AlphaBeta):
    """
    AlphaBeta法でテーブル評価値を使って次の手を決める
    """
    def __init__(self, depth=3, corner=50, c=-20, a=0, b=-1, x=-25, o=-5, w1=10000, w2=16, w3=2, w4=0.5, min_value=-10000000, max_value=10000000):
        super().__init__(depth, w1, w2, w3, min_value, max_value)
        self.table = Table(8, corner, c, a, b, x, o)  # Table戦略を利用する
        self._W4 = w4

    @Measure.time
    @Timer.start(CPU_TIME)
    def next_move(self, color, board):
        """
        次の一手
        """
        if self.table.size != board.size:  # テーブルサイズの調整
            self.table.set_table(board.size)

        next_color = 'white' if color == 'black' else 'black'
        best_move, alpha, beta = None, self._MIN, self._MAX

        # 打てる手の中から評価値の最も高い手を選ぶ
        for move in board.get_possibles(color).keys():
            board.put_stone(color, *move)                                            # 一手打つ
            score = -self.get_score(next_color, board, -beta, -alpha, self.depth-1)  # 評価値を取得
            board.undo()                                                             # 打った手を戻す

            if Timer.is_timeout(self):
                best_move = move if best_move is None else best_move
                break
            else:
                if score > alpha:  # 最善手を更新
                    alpha = score
                    best_move = move

        return best_move

    @Measure.countup
    @Timer.timeout
    def get_score(self, color, board, alpha, beta, depth):
        """
        評価値の取得
        """
        # ゲーム終了 or 最大深さに到達
        possibles_b = board.get_possibles('black', True)
        possibles_w = board.get_possibles('white', True)
        is_game_end =  True if not possibles_b and not possibles_w else False

        if is_game_end or depth <= 0:
            sign = 1 if color == 'black' else -1
            score = self.evaluate(board, possibles_b, possibles_w) * sign
            score += self.table.get_score(color, board) * self._W4
            return score

        # パスの場合
        possibles = possibles_b if color == 'black' else possibles_w
        next_color = 'white' if color == 'black' else 'black'

        if not possibles:
            return -self.get_score(next_color, board, -beta, -alpha, depth)

        # 評価値を算出
        for move in possibles.keys():
            board.put_stone(color, *move)
            score = -self.get_score(next_color, board, -beta, -alpha, depth-1)
            board.undo()

            if Timer.is_timeout(self):
                break
            else:
                alpha = max(alpha, score)  # 最大値を選択
                if alpha >= beta:  # 枝刈り
                    break

        return alpha


class AlphaBetaT1(AlphaBetaT):
    """
    AlphaBeta法でテーブル評価値を使って次の手を決める(1手読み)
    """
    def __init__(self, depth=1):
        super().__init__(depth)


class AlphaBetaT2(AlphaBetaT):
    """
    AlphaBeta法でテーブル評価値を使って次の手を決める(2手読み)
    """
    def __init__(self, depth=2):
        super().__init__(depth)


class AlphaBetaT3(AlphaBetaT):
    """
    AlphaBeta法でテーブル評価値を使って次の手を決める(3手読み)
    """
    def __init__(self, depth=3):
        super().__init__(depth)


class AlphaBetaT4(AlphaBetaT):
    """
    AlphaBeta法でテーブル評価値を使って次の手を決める(4手読み)
    """
    def __init__(self, depth=4):
        super().__init__(depth)


class AlphaBetaT5(AlphaBetaT):
    """
    AlphaBeta法でテーブル評価値を使って次の手を決める(5手読み)
    """
    def __init__(self, depth=5):
        super().__init__(depth)


class AlphaBetaTI(AlphaBetaT):
    """
    AlphaBetaTに反復深化法を適用して次の手を決める
    """
    @Measure.time
    @Timer.start(CPU_TIME)
    def next_move(self, color, board):
        """
        次の一手
        """
        next_color = 'white' if color == 'black' else 'black'
        best_move = None

        # 深さ2から始めて徐々に深く読んでいく
        depth = 2

        while True:
            alpha, beta = self._MIN, self._MAX

            # 前回の最善手を最初に調べる
            moves = list(board.get_possibles(color).keys())
            if best_move is not None:
                moves.remove(best_move)
                moves.insert(0, best_move)

            # 打てる手の中から評価値の最も高い手を選ぶ
            for move in moves:
                board.put_stone(color, *move)                                       # 一手打つ
                score = -self.get_score(next_color, board, -beta, -alpha, depth-1)  # 評価値を取得
                board.undo()                                                        # 打った手を戻す

                if Timer.is_timeout(self):
                    best_move = move if best_move is None else best_move
                    break
                else:
                    if score > alpha:  # 最善手を更新
                        alpha = score
                        best_move = move

            if Timer.is_timeout(self):
                break

            depth += 1

        return best_move


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
        [0, -1, -1, 0],
        [-1, -1, -1, -1],
        [-1, -1, -1, -1],
        [0, -1, -1, 0],
    ]
    assert (table4.table == np.array(table4_ret)).all()

    table8 = Table(8)
    table8_ret = [
        [50, -20, -1, -1, -1, -1, -20, 50],
        [-20, -25, -5, -5, -5, -5, -25, -20],
        [-1, -5, 0, -1, -1, 0, -5, -1],
        [-1, -5, -1, -1, -1, -1, -5, -1],
        [-1, -5, -1, -1, -1, -1, -5, -1],
        [-1, -5, 0, -1, -1, 0, -5, -1],
        [-20, -25, -5, -5, -5, -5, -25, -20],
        [50, -20, -1, -1, -1, -1, -20, 50],
    ]
    assert (table8.table == np.array(table8_ret)).all()

    table16 = Table(16)
    table16_ret = [
        [50, -20, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -20, 50],
        [-20, -25, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -25, -20],
        [-1, -5, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -5, -1],
        [-1, -5, -1, -25, -5, -5, -5, -5, -5, -5, -5, -5, -25, -1, -5, -1],
        [-1, -5, -1, -5, 0, -1, -1, -1, -1, -1, -1, 0, -5, -1, -5, -1],
        [-1, -5, -1, -5, -1, -25, -5, -5, -5, -5, -25, -1, -5, -1, -5, -1],
        [-1, -5, -1, -5, -1, -5, 0, -1, -1, 0, -5, -1, -5, -1, -5, -1],
        [-1, -5, -1, -5, -1, -5, -1, -1, -1, -1, -5, -1, -5, -1, -5, -1],
        [-1, -5, -1, -5, -1, -5, -1, -1, -1, -1, -5, -1, -5, -1, -5, -1],
        [-1, -5, -1, -5, -1, -5, 0, -1, -1, 0, -5, -1, -5, -1, -5, -1],
        [-1, -5, -1, -5, -1, -25, -5, -5, -5, -5, -25, -1, -5, -1, -5, -1],
        [-1, -5, -1, -5, 0, -1, -1, -1, -1, -1, -1, 0, -5, -1, -5, -1],
        [-1, -5, -1, -25, -5, -5, -5, -5, -5, -5, -5, -5, -25, -1, -5, -1],
        [-1, -5, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -5, -1],
        [-20, -25, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -25, -20],
        [50, -20, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -20, 50],
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

    # MinMax
    print('--- Test For MinMax Strategy ---')
    board8 = Board(8)
    minmax = MinMax()
    assert minmax.depth == 3
    print(board8)
    b = board8.get_possibles('black', True)
    w = board8.get_possibles('white', True)
    assert minmax.evaluate(board8, b, w) == 0

    board8.put_stone('black', 3, 2)
    board8.put_stone('white', 2, 4)
    print(board8)
    b = board8.get_possibles('black', True)
    w = board8.get_possibles('white', True)
    assert minmax.evaluate(board8, b, w) == 2

    board8.put_stone('black', 1, 5)
    board8.put_stone('white', 1, 4)
    board8.put_stone('black', 2, 5)
    board8.put_stone('white', 1, 6)
    board8.put_stone('black', 0, 7)
    print(board8)
    b = board8.get_possibles('black', True)
    w = board8.get_possibles('white', True)
    assert minmax.evaluate(board8, b, w) == 22

    board8.put_stone('black', 1, 3)
    board8.put_stone('black', 2, 3)
    board8.put_stone('black', 4, 5)
    print(board8)
    b = board8.get_possibles('black', True)
    w = board8.get_possibles('white', True)
    assert minmax.evaluate(board8, b, w) == 10014

    from board import BitBoard
    print('- bitboard -')
    bitboard8 = BitBoard(8)
    bitboard8.put_stone('black', 3, 2)
    print(bitboard8)
    assert minmax.get_score('white', bitboard8, 2) == 6
    assert minmax.get_score('white', bitboard8, 3) == -2

    print(bitboard8)
    assert minmax.next_move('white', bitboard8) == (2, 4)
    bitboard8.put_stone('white', 2, 4)
    bitboard8.put_stone('black', 5, 5)
    bitboard8.put_stone('white', 4, 2)
    bitboard8.put_stone('black', 5, 2)
    bitboard8.put_stone('white', 5, 4)
    print(bitboard8)
    assert minmax.next_move('black', bitboard8) == (2, 2)

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
    assert negamax.evaluate(board8, b, w) == 10014

    from board import BitBoard
    print('- bitboard -')
    bitboard8 = BitBoard(8)
    bitboard8.put_stone('black', 3, 2)

    Measure.count['NegaMax'] = 0
    Timer.timeout_flag['NegaMax'] = False
    Timer.deadline['NegaMax'] = time.time() + CPU_TIME
    assert negamax.get_score('white', bitboard8, 2) == -6
    assert Measure.count['NegaMax'] == 18

    Measure.count['NegaMax'] = 0
    Timer.timeout_flag['NegaMax'] = False
    Timer.deadline['NegaMax'] = time.time() + CPU_TIME
    assert negamax.get_score('white', bitboard8, 3) == 2
    assert Measure.count['NegaMax'] == 79

    Measure.count['NegaMax'] = 0
    Timer.timeout_flag['NegaMax'] = False
    Timer.deadline['NegaMax'] = time.time() + CPU_TIME
    assert negamax.get_score('white', bitboard8, 4) == -4
    assert Measure.count['NegaMax'] == 428

    Measure.count['NegaMax'] = 0
    Timer.timeout_flag['NegaMax'] = False
    Timer.deadline['NegaMax'] = time.time() + 5
    assert negamax.get_score('white', bitboard8, 5) == 2
    assert Measure.count['NegaMax'] == 2478

    Measure.count['NegaMax'] = 0
    Timer.timeout_flag['NegaMax'] = False
    Timer.deadline['NegaMax'] = time.time() + 5
    assert negamax.get_score('white', bitboard8, 6) == -4
    assert Measure.count['NegaMax'] == 16251

    print(bitboard8)
    assert negamax.next_move('white', bitboard8) == (2, 4)

    bitboard8.put_stone('white', 2, 4)
    bitboard8.put_stone('black', 5, 5)
    bitboard8.put_stone('white', 4, 2)
    bitboard8.put_stone('black', 5, 2)
    bitboard8.put_stone('white', 5, 4)
    print(bitboard8)

    Measure.count['NegaMax'] = 0
    Timer.timeout_flag['NegaMax'] = False
    Timer.deadline['NegaMax'] = time.time() + 5
    assert negamax.next_move('black', bitboard8) == (2, 2)
    assert Measure.count['NegaMax'] == 575

    Measure.count['NegaMax'] = 0
    negamax.depth = 2
    Timer.timeout_flag['NegaMax'] = False
    Timer.deadline['NegaMax'] = time.time() + 2
    assert negamax.next_move('black', bitboard8) == (2, 2)
    assert Measure.count['NegaMax'] == 70

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
    assert alphabeta.evaluate(board8, b, w) == 10014

    from board import BitBoard
    print('- bitboard -')
    bitboard8 = BitBoard(8)
    bitboard8.put_stone('black', 3, 2)

    Measure.count['AlphaBeta'] = 0
    Timer.timeout_flag['AlphaBeta'] = False
    Timer.deadline['AlphaBeta'] = time.time() + CPU_TIME
    assert alphabeta.get_score('white', bitboard8, -10000000, 10000000, 2) == -6
    assert Measure.count['AlphaBeta'] == 16

    Measure.count['AlphaBeta'] = 0
    Timer.timeout_flag['AlphaBeta'] = False
    Timer.deadline['AlphaBeta'] = time.time() + CPU_TIME
    assert alphabeta.get_score('white', bitboard8, -10000000, 10000000, 3) == 2
    assert Measure.count['AlphaBeta'] == 58

    Measure.count['AlphaBeta'] = 0
    Timer.timeout_flag['AlphaBeta'] = False
    Timer.deadline['AlphaBeta'] = time.time() + CPU_TIME
    assert alphabeta.get_score('white', bitboard8, -10000000, 10000000, 4) == -4
    assert Measure.count['AlphaBeta'] == 226

    Measure.count['AlphaBeta'] = 0
    Timer.timeout_flag['AlphaBeta'] = False
    Timer.deadline['AlphaBeta'] = time.time() + 1
    assert alphabeta.get_score('white', bitboard8, -10000000, 10000000, 5) == 2
    assert Measure.count['AlphaBeta'] == 617

    Measure.count['AlphaBeta'] = 0
    Timer.timeout_flag['AlphaBeta'] = False
    Timer.deadline['AlphaBeta'] = time.time() + 3
    assert alphabeta.get_score('white', bitboard8, -10000000, 10000000, 6) == -4
    assert Measure.count['AlphaBeta'] == 1865

    print(bitboard8)
    assert alphabeta.next_move('white', bitboard8) == (2, 4)

    print('* black check')
    bitboard8.put_stone('white', 2, 4)
    bitboard8.put_stone('black', 5, 5)
    bitboard8.put_stone('white', 4, 2)
    bitboard8.put_stone('black', 5, 2)
    bitboard8.put_stone('white', 5, 4)
    print(bitboard8)

    Measure.count['AlphaBeta'] = 0
    Timer.timeout_flag['AlphaBeta'] = False
    Timer.deadline['AlphaBeta'] = time.time() + 3
    assert alphabeta.next_move('black', bitboard8) == (2, 2)
    assert Measure.count['AlphaBeta'] == 170

    Measure.count['AlphaBeta'] = 0
    alphabeta.depth = 2
    Timer.timeout_flag['AlphaBeta'] = False
    Timer.deadline['AlphaBeta'] = time.time() + 3
    assert alphabeta.next_move('black', bitboard8) == (2, 2)
    assert Measure.count['AlphaBeta'] == 29

    # AlphaBetaT
    print('--- Test For AlphaBetaT Strategy ---')
    print('- bitboard -')
    alphabetat = AlphaBetaT()
    bitboard8 = BitBoard(8)
    bitboard8.put_stone('black', 3, 2)
    bitboard8.put_stone('white', 2, 4)
    bitboard8.put_stone('black', 5, 5)
    bitboard8.put_stone('white', 4, 2)
    bitboard8.put_stone('black', 5, 2)
    bitboard8.put_stone('white', 5, 4)
    print(bitboard8)

    Measure.count['AlphaBetaT'] = 0
    Timer.timeout_flag['AlphaBetaT'] = False
    Timer.deadline['AlphaBetaT'] = time.time() + 3
    assert alphabetat.next_move('black', bitboard8) == (2, 2)
    assert Measure.count['AlphaBetaT'] == 148

    # AlphaBetaTI
    print('--- Test For AlphaBetaTI Strategy ---')
    print('- bitboard -')
    alphabetati = AlphaBetaTI()
    bitboard8 = BitBoard(8)
    bitboard8.put_stone('black', 3, 2)
    bitboard8.put_stone('white', 2, 4)
    bitboard8.put_stone('black', 5, 5)
    bitboard8.put_stone('white', 4, 2)
    bitboard8.put_stone('black', 5, 2)
    bitboard8.put_stone('white', 5, 4)
    print(bitboard8)

    Measure.count['AlphaBetaTI'] = 0
    Timer.timeout_flag['AlphaBetaTI'] = False
    assert alphabetati.next_move('black', bitboard8) == (5, 3)
    assert Measure.count['AlphaBetaTI'] >= 1900
