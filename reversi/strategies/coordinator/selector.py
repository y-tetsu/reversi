"""Selector
"""

from reversi.strategies.common import AbstractSelector


class Selector(AbstractSelector):
    """Selector
    """
    def select_moves(self, color, board, moves, scores, depth):
        """select_moves
        """
        return moves


class Selector_W(Selector):
    """Selector_W

           ワースト値に基づいて手を絞る
    """
    def __init__(self, depth=3, limit=3):
        self.depth = depth
        self.limit = limit

    def select_moves(self, color, board, moves, scores, depth):
        """select_moves
        """
        moves = super().select_moves(color, board, moves, scores, depth)

        if depth >= self.depth:  # 一定以上の深さの場合
            worst_score = min([score for score in scores.values()])
            worst_moves = [key for key in scores.keys() if scores[key] == worst_score]

            # 次の手の候補数がリミット以上の間は絞る
            if len(moves) - len(worst_moves) >= self.limit:
                for worst_move in worst_moves:
                    moves.remove(worst_move)  # 最もスコアの低い手を削除

        return moves
