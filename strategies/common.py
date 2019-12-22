#!/usr/bin/env python
"""
共通処理
"""

import abc


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
