#!/usr/bin/env python
"""
リバーシの戦略初期版(デバッグ時の対戦相手)
"""

import random

from reversi.strategies.common import Timer, Measure, CPU_TIME, AbstractStrategy
from reversi.strategies.table import Table


class MinMax_(AbstractStrategy):
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
        for move in board.get_legal_moves(color, cache=True).keys():
            board.put_disc(color, *move)                             # 一手打つ
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
        legal_moves_b = board.get_legal_moves('black')  # 黒の打てる場所
        legal_moves_w = board.get_legal_moves('white')  # 白の打てる場所
        is_game_end = True if not legal_moves_b and not legal_moves_w else False

        if is_game_end or depth <= 0:
            return self.evaluate(board, legal_moves_b, legal_moves_w)

        # パスの場合
        legal_moves = legal_moves_b if color == 'black' else legal_moves_w
        next_color = 'white' if color == 'black' else 'black'

        if not legal_moves:
            return self.get_score(next_color, board, depth)

        # 評価値を算出
        best_score = self._MIN if color == 'black' else self._MAX

        for move in legal_moves.keys():
            board.put_disc(color, *move)
            score = self.get_score(next_color, board, depth-1)
            board.undo()

            # ベストスコア取得
            best_score = max(best_score, score) if color == 'black' else min(best_score, score)

        return best_score

    def evaluate(self, board, legal_moves_b, legal_moves_w):
        """
        評価値の算出
        """
        ret = 0

        # 対局終了時
        if not legal_moves_b and not legal_moves_w:
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
        black_num = len(list(legal_moves_b.keys()))
        white_num = len(list(legal_moves_w.keys()))

        ret += (black_num - white_num) * self._W3

        return ret


class NegaMax_(MinMax_):
    """
    NegaMax法で次の手を決める
    """
    @Measure.time
    @Timer.start(CPU_TIME, -10000000)
    def next_move(self, color, board):
        """
        次の一手
        """
        next_color = 'white' if color == 'black' else 'black'
        moves, max_score = {}, self._MIN

        # 打てる手の中から評価値の最も高い手を選ぶ
        for move in board.get_legal_moves(color, cache=True).keys():
            board.put_disc(color, *move)                              # 一手打つ
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
        legal_moves_b = board.get_legal_moves('black')
        legal_moves_w = board.get_legal_moves('white')
        is_game_end = True if not legal_moves_b and not legal_moves_w else False

        if is_game_end or depth <= 0:
            return self.evaluate(color, board, legal_moves_b, legal_moves_w)

        # パスの場合
        legal_moves = legal_moves_b if color == 'black' else legal_moves_w
        next_color = 'white' if color == 'black' else 'black'

        if not legal_moves:
            return -self.get_score(next_color, board, depth)

        # 評価値を算出
        max_score = self._MIN

        for move in legal_moves.keys():
            board.put_disc(color, *move)
            score = -self.get_score(next_color, board, depth-1)
            board.undo()

            if Timer.is_timeout(self):
                break
            else:
                max_score = max(max_score, score)  # 最大値を選択

        return max_score

    def evaluate(self, color, board, legal_moves_b, legal_moves_w):
        """
        評価値の算出
        """
        sign = 1 if color == 'black' else -1

        return super().evaluate(board, legal_moves_b, legal_moves_w) * sign


class AlphaBeta_(NegaMax_):
    """
    AlphaBeta法で次の手を決める
    """
    @Measure.time
    @Timer.start(CPU_TIME, -10000000)
    def next_move(self, color, board):
        """
        次の一手
        """
        moves = board.get_legal_moves(color, cache=True).keys()  # 手の候補

        return self.get_best_move(color, board, moves, self.depth)

    def get_best_move(self, color, board, moves, depth):
        """
        最善手を選ぶ
        """
        best_move, alpha, beta = None, self._MIN, self._MAX

        # 打てる手の中から評価値の最も高い手を選ぶ
        for move in moves:
            score = self.get_score(move, color, board, alpha, beta, depth)

            if Timer.is_timeout(self):
                best_move = move if best_move is None else best_move
                break
            else:
                if score > alpha:  # 最善手を更新
                    alpha = score
                    best_move = move

        return best_move

    def get_score(self, move, color, board, alpha, beta, depth):
        """
        手を打った時の評価値を取得
        """
        board.put_disc(color, *move)                                         # 一手打つ
        next_color = 'white' if color == 'black' else 'black'                # 相手の色
        score = -self._get_score(next_color, board, -beta, -alpha, depth-1)  # 評価値を取得
        board.undo()                                                         # 打った手を戻す

        return score

    @Measure.countup
    @Timer.timeout
    def _get_score(self, color, board, alpha, beta, depth):
        """
        評価値の取得
        """
        # ゲーム終了 or 最大深さに到達
        legal_moves_b = board.get_legal_moves('black')
        legal_moves_w = board.get_legal_moves('white')
        is_game_end = True if not legal_moves_b and not legal_moves_w else False

        if is_game_end or depth <= 0:
            return self.evaluate(color, board, legal_moves_b, legal_moves_w)

        # パスの場合
        legal_moves = legal_moves_b if color == 'black' else legal_moves_w
        next_color = 'white' if color == 'black' else 'black'

        if not legal_moves:
            return -self._get_score(next_color, board, -beta, -alpha, depth)

        # 評価値を算出
        for move in legal_moves.keys():
            board.put_disc(color, *move)
            score = -self._get_score(next_color, board, -beta, -alpha, depth-1)
            board.undo()

            if Timer.is_timeout(self):
                break
            else:
                alpha = max(alpha, score)  # 最大値を選択
                if alpha >= beta:  # 枝刈り
                    break

        return alpha


class AB_T(AlphaBeta_):
    """
    AlphaBeta法でテーブル評価値を使って次の手を決める
    """
    def __init__(self, depth=3, corner=50, c=-20, a=0, b=-1, x=-25, o=-5, w1=10000, w2=16, w3=2, w4=0.5, min_value=-10000000, max_value=10000000):
        super().__init__(depth, w1, w2, w3, min_value, max_value)
        self.table = Table(8, corner, c, a, b, x, o)  # Table戦略を利用する
        self._W4 = w4

    @Measure.time
    @Timer.start(CPU_TIME, -10000000)
    def next_move(self, color, board):
        """
        次の一手
        """
        if self.table.size != board.size:  # テーブルサイズの調整
            self.table.set_table(board.size)

        return super().next_move(color, board)

    def evaluate(self, color, board, legal_moves_b, legal_moves_w):
        """
        評価値の算出
        """
        ret = super().evaluate(color, board, legal_moves_b, legal_moves_w)  # 元の評価
        ret += self.table.get_score(color, board) * self._W4            # テーブル評価を追加

        return ret


class MinMax2(MinMax_):
    """
    MinMax法で次の手を決める(2手読み)
    """
    def __init__(self, depth=2):
        super().__init__(depth)


class NegaMax3(NegaMax_):
    """
    NegaMax法で次の手を決める(3手読み)
    """
    def __init__(self, depth=3):
        super().__init__(depth)


class AlphaBeta4(AlphaBeta_):
    """
    AlphaBeta法で次の手を決める(4手読み)
    """
    def __init__(self, depth=4):
        super().__init__(depth)


class AB_T4(AB_T):
    """
    AlphaBeta法でテーブル評価値を使って次の手を決める(4手読み)
    """
    def __init__(self, depth=4):
        super().__init__(depth)


class AB_TI(AB_T):
    """
    AB_Tに反復深化法を適用して次の手を決める
    """
    def __init__(self, depth=2, corner=50, c=-20, a=0, b=-1, x=-25, o=-5, w1=10000, w2=16, w3=2, w4=0.5, min_value=-10000000, max_value=10000000):
        super().__init__(depth, corner, c, a, b, x, o, w1, w2, w3, w4, min_value, max_value)

    @Measure.time
    @Timer.start(CPU_TIME, -10000000)
    def next_move(self, color, board):
        """
        次の一手
        """
        if self.table.size != board.size:  # テーブルサイズの調整
            self.table.set_table(board.size)

        depth, best_move = self.depth, None

        while True:
            moves = list(board.get_legal_moves(color, cache=True).keys())

            # 前回の最善手を優先的に
            if best_move is not None:
                moves.remove(best_move)
                moves.insert(0, best_move)

            # 4隅はさらに優先的に調べる
            for corner in [(0, 0), (0, board.size-1), (board.size-1, 0), (board.size-1, board.size-1)]:
                if corner in moves:
                    moves.remove(corner)
                    moves.insert(0, corner)

            best_move = super().get_best_move(color, board, moves, depth)  # 最善手

            if Timer.is_timeout(self):  # タイムアウト
                break

            depth += 1  # 次の読みの深さ

        return best_move
