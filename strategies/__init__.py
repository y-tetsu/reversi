#!/usr/bin/env python
from strategies.timer import Timer
from strategies.measure import Measure
from strategies.input import ConsoleUserInput, WindowUserInput
from strategies.easy import Random, Greedy, Unselfish, SlowStarter, Table
from strategies.minmax import MinMax1, MinMax2, MinMax3, MinMax4, MinMax1_T, MinMax2_T, MinMax3_T, MinMax4_T, MinMax1_TP, MinMax2_TP, MinMax3_TP, MinMax4_TP, MinMax1_TPO, MinMax2_TPO, MinMax3_TPO, MinMax4_TPO
from strategies.negamax import NegaMax1, NegaMax2, NegaMax3, NegaMax4
from strategies.alphabeta import AlphaBeta1, AlphaBeta2, AlphaBeta3, AlphaBeta4, AlphaBeta5, AB_T1, AB_T2, AB_T3, AB_T4, AB_T5, AB_TI
