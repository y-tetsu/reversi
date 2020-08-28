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
                This player chooses a move in the monte-carlo method.

            MinMax
                This player chooses a move by reading 2 moves ahead in the minmax method.

            NegaMax
                This player chooses a move by reading 3 moves ahead in the negamax method.

        (Level 3)
            AlphaBeta
                This player chooses a move by reading 4 moves ahead for as long as time in the alpha-beta method.

            Joseki
                In addition to AlphaBeta, this player chooses a move according to standard tactics in the early stages.

            FullReading
                In addition to Joseki, this player chooses a move by reading the difference in the number of discs
                from the last 9 moves to the final phase of the game.

        (Level 4)
            Iterative
                This player applies the iterative-deepening method to FullReading
                and reads moves gradually and deeply for as long as it takes.
                When deepening the reading, this plyer is increasing efficiency by reading the last best move first.

            Edge
                In addition to Iterative, this player chooses a move that increases the definite disc
                by considering the 4-edge pattern.

            Switch
                Each parameter of Edge is strengthened using a genetic algorithm,
                and the parameter is switched to 5 levels according to the number of steps.
                Therefore, the move that matches the progress of the game is selected.
                The search method is also changed from the alpha-beta method to the negacout method,
                and the board candidates are rearranged so as to preferentially search for
                a move with a larger number of possible moves to read the board more efficiently.
                In addition, read the discs difference from the last 10 moves to the final phase of the game.
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
        'Joseki': strategies.AlphaBeta4J_TPW(),
        'FullReading': strategies.AlphaBeta4F9J_TPW(),
        'Iterative': strategies.AbIF9J_B_TPW(),
        'Edge': strategies.AbIF9J_B_TPWE(),
        'Switch': strategies.SwitchNsIF10J_B_TPWE(),
    }
).start()
