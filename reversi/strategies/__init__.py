#!/usr/bin/env python
from reversi.strategies.common import CPU_TIME, Timer, Measure, AbstractStrategy, AbstractScorer, AbstractEvaluator, AbstractSorter, AbstractSelector
from reversi.strategies.user import ConsoleUserInput, WindowUserInput
from reversi.strategies.easy import Random, Greedy, Unselfish, SlowStarter
from reversi.strategies.table import Table
from reversi.strategies.minmax import MinMax, MinMax1_T, MinMax2_T, MinMax3_T, MinMax4_T, MinMax1_TP, MinMax2_TP, MinMax3_TP, MinMax4_TP, MinMax1_TPO, MinMax2_TPO, MinMax3_TPO, MinMax4_TPO, MinMax2_TPW, MinMax3_TPW, MinMax4_TPW, MinMax1_TPOW, MinMax2_TPOW, MinMax3_TPOW, MinMax4_TPOW
from reversi.strategies.negamax import _NegaMax, NegaMax, NegaMax1_TPOW, NegaMax2_TPOW, NegaMax3_TPW, NegaMax3_TPOW, NegaMax4_TPOW
from reversi.strategies.alphabeta import _AlphaBeta, AlphaBeta, AlphaBeta3_TPW, AlphaBeta4_TPW
from reversi.strategies.negascout import _NegaScout, NegaScout, NegaScout3_TPW, NegaScout3_TPOW, NegaScout4_TPW
from reversi.strategies.iterative import IterativeDeepning, AbI_B_TPW, NsI_B_TPW
from reversi.strategies.fullreading import _FullReading, FullReading, AlphaBeta4F9_TPW, AbIF9_B_TPW, NsIF10_B_TPW, NsIF11_B_TPW, NsIF12_B_TPW, RandomF11
from reversi.strategies.joseki import Usagi, Tora, Ushi, Nezumi, Neko, Hitsuji, AlphaBeta4J_TPW, AlphaBeta4F9J_TPW, AbIF9J_B_TPW, AbIF9J_B_TPWE, AbIF9J_B_TPWEC, NsIF9J_B_TPW, NsIF9J_B_TPWE, SwitchNsIF9J_B_TPW, SwitchNsIF9J_B_TPWE
from reversi.strategies.montecarlo import MonteCarlo, MonteCarlo30, MonteCarlo100, MonteCarlo1000
from reversi.strategies.proto import MinMax2, NegaMax3, AlphaBeta4, AB_T4, AB_TI
from reversi.strategies.randomopening import RandomOpening, MinMax2Ro_T, MinMax1Ro_TPW, MinMax1Ro_TPWE, MinMax1Ro_TPWEC, MinMax1Ro_PWE, MinMax1Ro_TPW2, MinMax2Ro_TPW, MinMax2Ro_TPWE, MinMax2Ro_TPWEC, MinMax3Ro_T, MinMax3Ro_TP, MinMax3Ro_TPW, MinMax3Ro_TPOW, _NegaMax3Ro_TPW, NegaMax3Ro_TPW, NegaMax3Ro_TPOW, NegaScout3Ro_TPW, NegaScout3Ro_TPOW, AlphaBeta4Ro_TPW, AlphaBeta4Ro_TPWE, AlphaBeta4JRo_TPW, AlphaBeta4F9Ro_TPW, AlphaBeta4F9JRo_TPW, NegaScout4Ro_TPW, NegaScout4Ro_TPWE, AB_TI_Ro, AbIF9JRo_B_TPW, AbIF9JRo_B_TPWE, AbIF9JRo_B_TPWEC, NsIF9JRo_B_TPW, NsIF9JRo_B_TPW2, NsIF9JRo_B_TPWE, SwitchNsIF9JRo_B_TPW, SwitchNsIF9JRo_B_TPWE
from reversi.strategies.external import External
