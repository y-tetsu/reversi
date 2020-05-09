#!/usr/bin/env python
from reversi.board import Board, BitBoard, MIN_BOARD_SIZE, MAX_BOARD_SIZE
from reversi.player import Player
from reversi.display import ConsoleDisplay, NoneDisplay, WindowDisplay
from reversi.game import Game
from reversi.window import Window
from reversi.app import Reversi, Reversic
from reversi.simulator import Simulator
import reversi.strategies
import reversi.genetic_algorithm
