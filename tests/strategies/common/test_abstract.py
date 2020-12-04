"""Tests of abstract.py
"""

import unittest

from reversi.strategies.common import AbstractStrategy, AbstractScorer, AbstractEvaluator, AbstractOrderer, AbstractSelector


class TestAbstract(unittest.TestCase):
    """abstract
    """
    def test_abstract_strategy(self):
        AbstractStrategy.next_move("self", "color", "board")

    def test_abstract_scorer(self):
        AbstractScorer.get_score("self", "*args", "**kwargs")

    def test_abstract_evaluator(self):
        AbstractEvaluator.evaluate("self", "*args", "**kwargs")

    def test_abstract_orderer(self):
        AbstractOrderer.move_ordering("self", "*args", "**kwargs")

    def test_abstract_selector(self):
        AbstractSelector.select_moves("self", "*args", "**kwargs")
