#!/usr/bin/env python
"""
共通
"""

import abc


CPU_TIME = 0.5  # CPUの持ち時間(s)


class AbstractStrategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def next_move(self, color, board):
        pass
