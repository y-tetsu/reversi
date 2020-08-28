"""Switch
"""

from reversi.strategies.common import Measure, AbstractStrategy


class SwitchSizeError(Exception):
    """
    入力サイズのエラー
    """
    pass


class _Switch_(AbstractStrategy):
    """
    複数戦略を切り替える
    """
    def __init__(self, turns=None, strategies=None):
        if len(turns) != len(strategies):
            raise SwitchSizeError

        self.turns = turns
        self.strategies = strategies

    def next_move(self, color, board):
        """
        次の一手
        """
        disc_num = board._black_score + board._white_score

        # 現在の手数が閾値以下
        strategy = self.strategies[-1]

        for i, turn in enumerate(self.turns):
            if disc_num - 4 <= turn:
                strategy = self.strategies[i]
                break

        return strategy.next_move(color, board)


class Switch(_Switch_):
    """Switch + Measure
    """
    @Measure.time
    def next_move(self, color, board):
        """next_move
        """
        return super().next_move(color, board)
