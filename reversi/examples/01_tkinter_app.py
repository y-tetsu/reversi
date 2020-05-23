#!/usr/bin/env python
"""Reversi GUI Application using tkinter

    This is a reversi GUI Application using tkinter.

    AI players:
        (Level 1)
            Unselfish
                This player try to take as little as possible.

            Random
                This player choose a move at random.

            Greedy
                This player try to take as much as possible.

            SlowStarter
                This player become Unselfish in the early stages and then Greedy.

        (Level 2)
            Table
                This player evaluates the board at the weight table and choose a move.
                Take as little as possible, aim at the corners and avoid near the corners.

            MonteCarlo
                This player chooses his moves using the Monte Carlo method.

            MinMax
                This player chooses a move by reading 2 moves ahead in the minmax method.

            NegaMax
                This player chooses a move by reading 3 moves ahead in the negamax method.

        (Level 3)
            AlphaBeta
                This player chooses a move by reading 4 moves ahead for as long as time in the alpha-beta method.

            Joseki
                In addition to AlphaBeta, this player chooses a move according to standard tactics.

            FullReading
                In addition to Joseki, this player chooses a move by reading the stone difference
                from the last 9 moves to the final phase of the game.

        (Level 4)
            Iterative
                This player applies the iterative deepening method to FullReading
                and reads moves gradually and deeply for as long as it takes.

            Edge
                In addition to Iterative, this player chooses a move that increases the definite disc
                by considering the 4-edge pattern.
"""

from reversi import Reversi, strategies


Reversi(
    {
        'Unselfish': strategies.Unselfish(),
        'Random': strategies.Random(),
        'Greedy': strategies.Greedy(),
        'SlowStarter': strategies.SlowStarter(),
        'Table': strategies.Table(),
        'MonteCarlo': strategies.MonteCarlo1000(),
        'MinMax': strategies.MinMax2_TPW(),
        'NegaMax': strategies.NegaMax3_TPW(),
        'AlphaBeta': strategies.AlphaBeta4_TPW(),
        'Joseki' : strategies.AlphaBeta4J_TPW(),
        'FullReading' : strategies.AlphaBeta4F9J_TPW(),
        'Iterative': strategies.AbIF9J_B_TPW(),
        'Edge': strategies.AbIF9J_B_TPWE(),
    }
).start()
