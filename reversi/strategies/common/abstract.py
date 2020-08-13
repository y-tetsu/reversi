#!/usr/bin/env python
"""
基底クラス
"""

import abc


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


class AbstractOrderer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def move_ordering(self, *args, **kwargs):
        pass


class AbstractSelector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def select_moves(self, *args, **kwargs):
        pass
