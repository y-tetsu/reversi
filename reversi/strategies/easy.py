"""Easy strategy
"""

import random

from reversi.strategies.common import AbstractStrategy


class Random(AbstractStrategy):
    """Random strategy
    """
    def next_move(self, color, board):
        """次の手をランダムに決定します

        Args:
            color: プレイヤーのディスクの色
            board: 現在のボードの状態

        Returns:
            ランダムに選ばれた合法的な手
        """
        moves = board.get_legal_moves(color)

        return random.choice(moves)


class Greedy(AbstractStrategy):
    """Greedy strategy
    
    可能な限り多くのディスクを取り、複数ある場合はランダムに選びます
    """
    def next_move(self, color, board):
        """次の手を貪欲に決定します

        Args:
            color: プレイヤーのディスクの色
            board: 現在のボードの状態

        Returns:
            最大数のディスクをひっくり返す手
        """
        legal_moves = board.get_legal_moves(color)
        max_count = max([len(board.get_flippable_discs(color, *move)) for move in legal_moves])
        moves = [move for move in legal_moves if len(board.get_flippable_discs(color, *move)) == max_count]

        return random.choice(moves)


class Unselfish(AbstractStrategy):
    """Unselfish strategy
    
    可能な限り少ないディスクを取り、複数ある場合はランダムに選びます
    """
    def next_move(self, color, board):
        """次の手を控えめに決定します

        Args:
            color: プレイヤーのディスクの色
            board: 現在のボードの状態

        Returns:
            最小数のディスクをひっくり返す手
        """
        legal_moves = board.get_legal_moves(color)
        min_count = min([len(board.get_flippable_discs(color, *move)) for move in legal_moves])
        moves = [move for move in legal_moves if len(board.get_flippable_discs(color, *move)) == min_count]

        return random.choice(moves)


class SlowStarter(AbstractStrategy):
    """SlowStarter strategy
    
    ゲームの進行状況が15%未満の場合はUnselfish、それ以外はGreedyを使用します
    """
    def __init__(self):
        self.unselfish = Unselfish()
        self.greedy = Greedy()

    def next_move(self, color, board):
        """ゲームの進行状況に基づいて次の手を決定します

        Args:
            color: プレイヤーのディスクの色
            board: 現在のボードの状態

        Returns:
            ゲームの進行状況に基づいて決定された手
        """
        squares = board.size**2
        blanks = sum([row.count(0) for row in board.get_board_info()])

        # 進行状況が15%未満の場合
        if (squares-blanks)/squares < 0.15:
            return self.unselfish.next_move(color, board)

        # それ以外の場合
        return self.greedy.next_move(color, board)
