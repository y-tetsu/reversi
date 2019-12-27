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


class AbstractScorer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_score(self, color, board):
        pass


class AbstractEvaluator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def evaluate(self, color, board):
        pass


class AbstractSelector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def select_moves(self, color, board, best_move, scores, depth):
        pass
