#!/usr/bin/env python
from reversi.strategies.coordinator.scorer import TableScorer, PossibilityScorer, OpeningScorer, WinLoseScorer, NumberScorer, EdgeScorer, CornerScorer
from reversi.strategies.coordinator.selector import Selector, Selector_W
from reversi.strategies.coordinator.sorter import Sorter, Sorter_B, Sorter_C, Sorter_O, Sorter_BC, Sorter_CB
from reversi.strategies.coordinator.evaluator import Evaluator_T, Evaluator_P, Evaluator_O, Evaluator_W, Evaluator_N, Evaluator_TP, Evaluator_TPO, Evaluator_NW, Evaluator_PW, Evaluator_TPW, Evaluator_TPOW, Evaluator_TPWE, Evaluator_TPWEC, Evaluator_PWE
