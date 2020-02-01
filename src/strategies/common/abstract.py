#!/usr/bin/env python
"""
基底クラス
"""

import abc


CPU_TIME = 0.5  # CPUの持ち時間(s)


class AbstractStrategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def next_move(self, color, board):
        pass


class AbstractScorer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_score(self, *args, **kwargs):
        pass


class AbstractEvaluator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def evaluate(self, *args, **kwargs):
        pass


class AbstractSorter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def sort_moves(self, *args, **kwargs):
        pass


class AbstractSelector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def select_moves(self, *args, **kwargs):
        pass
