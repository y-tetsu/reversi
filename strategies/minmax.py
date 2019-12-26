#!/usr/bin/env python
"""
オセロの戦略(MinMax)
"""

import sys
sys.path.append('../')

import random

from strategies.common import AbstractStrategy
from strategies.measure import Measure
from strategies.evaluator import Evaluator_T


class MinMax(AbstractStrategy):
    """
    MinMax法で次の手を決める
    """
    def __init__(self, depth=3, evaluator=None):
        self._MIN = -10000000
        self._MAX = 10000000

        self.depth = depth
        self.evaluator = evaluator

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
            return self.evaluator.evaluate(color, board, possibles_b, possibles_w)

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


class MinMax1_T(MinMax):
    """
    MinMax法でテーブル評価値により次の手を決める(1手読み)
    """
    def __init__(self, depth=1, evaluator=Evaluator_T()):
        super().__init__(depth, evaluator)


class MinMax2_T(MinMax):
    """
    MinMax法でテーブル評価値により次の手を決める(2手読み)
    """
    def __init__(self, depth=2, evaluator=Evaluator_T()):
        super().__init__(depth, evaluator)


class MinMax3_T(MinMax):
    """
    MinMax法でテーブル評価値により次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_T()):
        super().__init__(depth, evaluator)


class MinMax4_T(MinMax):
    """
    MinMax法でテーブル評価値により次の手を決める(3手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_T()):
        super().__init__(depth, evaluator)


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


class MinMax1(MinMax_):
    """
    MinMax法で次の手を決める(1手読み)
    """
    def __init__(self, depth=1):
        super().__init__(depth)


class MinMax2(MinMax_):
    """
    MinMax法で次の手を決める(2手読み)
    """
    def __init__(self, depth=2):
        super().__init__(depth)


class MinMax3(MinMax_):
    """
    MinMax法で次の手を決める(3手読み)
    """
    def __init__(self, depth=3):
        super().__init__(depth)


class MinMax4(MinMax_):
    """
    MinMax法で次の手を決める(4手読み)
    """
    def __init__(self, depth=4):
        super().__init__(depth)


if __name__ == '__main__':
    from board import Board
    print('--- Test For MinMax Strategy ---')
    board8 = Board(8)
    minmax = MinMax_()
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
