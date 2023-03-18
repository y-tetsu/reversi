<p align="center">
<img src="https://raw.githubusercontent.com/y-tetsu/reversi/images/reversi_v0_0_15.png" width="500px">
</p>

# reversi
[ [English](https://github.com/y-tetsu/reversi/blob/master/README.en.md) | [日本語](https://github.com/y-tetsu/reversi/blob/master/README.md)]<br>
<br>
**reversi** is a library for Reversi (Othello) for Python.<br>
You can easily program reversi AI and create applications.<br>
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
[![Build Status](https://travis-ci.org/y-tetsu/reversi.svg?branch=master)](https://travis-ci.org/y-tetsu/reversi)
[![codecov](https://codecov.io/gh/y-tetsu/reversi/branch/master/graph/badge.svg)](https://codecov.io/gh/y-tetsu/reversi)
<br>


## 目次
- [Overview](#Overview)
- [System Requirements](#System-Requirements)
- [How to Install](#How-to-Install)
- [How to Uninstall](#How-to-Uninstall)
- [Examples](#Examples)
- [How to use the library](#How-to-use-the-library)
    - [Basics](#Basics)
        - [Launching an Application](#Launching-an-Application)
        - [Adding an AI to your application](#Adding-an-AI-to-your-application)
        - [Programming an AI](#Programming-an-AI)
        - [Simulate a match between AIs](#Simulate-a-match-between-AIs)
    - [Objects](#Objects)
        - [How to use board object](#How-to-use-board-object)
        - [How to use color object](#How-to-use-color-object)
        - [How to use move object](#How-to-use-move-object)
    - [AI class](#AI-class)
        - [Simple-minded AI](#AI-class-Section)
        - [AI that chooses moves based on the position of squares](#AI-that-chooses-moves-based-on-the-position-of-squares)
        - [AI that chooses moves with a good chance of winning after playing multiple moves at random](#AI-that-chooses-moves-with-a-good-chance-of-winning-after-playing-multiple-moves-at-random)
        - [AI that reads the board several moves ahead and chooses moves](#AI-that-reads-the-board-several-moves-ahead-and-chooses-moves)
        - [How to customize the evaluation function](#How-to-customize-the-evaluation-function)
        - [How to create your own evaluation function](#How-to-create-your-own-evaluation-function)
        - [How to add joseki moves in the early game](#How-to-add-joseki-moves-in-the-early-game)
        - [How to switch AI based on move progression](#How-to-switch-AI-based-on-move-progression)
        - [How to add complete readings in endgame](#How-to-add-complete-readings-in-endgame)
- [How to play tkinter application](#How-to-play-tkinter-application)
    - [Game Introduction](#Game-Introduction)
    - [Download](#Download)
    - [Menu List](#Menu-List)
    - [Player Introduction](#Player-Introduction)
    - [Add Player](#Add-Player)
- [How to play console application](#How-to-play-console-application)
    - [Game Introduction](#Game-Introduction)
    - [Menu screen](#Menu-screen)
    - [Change Board](#Change-Board)
    - [Change Player](#Change-Player)
    - [Make a move](#Make-a-move)
- [If the installation does not work](#If-the-installation-does-not-work)
- [Footnotes](#Footnotes)
- [License](#License)


## Overview
**reversi** is a Reversi library made in <a id="return1">Python</a><sup>[1](#note1)</sup> that can be used with Python.<br>
After installing **reversi**, you can easily experiment with Reversi AI programming.<br>

Other uses include
- Create an application and play against your own AI.
- Use simulators to test the strength of AIs by playing them against each other.

[A Windows version of the application](#A-Windows-version-of-the-application) created using this library is also available.<br>
This one allows you to play a game of reversi for free immediately after downloading, with no installation required.<br>

<img src="https://raw.githubusercontent.com/y-tetsu/reversi/images/tkinter_app_demo_v0_0_15.gif" width="550px">

<img src="https://raw.githubusercontent.com/y-tetsu/reversi/images/console_app_demo4.gif" width="550px">

<img src="https://raw.githubusercontent.com/y-tetsu/reversi/images/simulator_demo.gif" width="550px">


## System Requirements
- Windows10 64bit<br>
- Display size 1366x768
- Processor 1.6GHz
- Memory 4.00GB
- [Python 3.7.6](https://www.python.org/downloads/release/python-376/)<br>
    - cython 0.29.15<br>
    - pyinstaller 3.6<br>
- [Microsoft Visual C++ 2019](https://visualstudio.microsoft.com/downloads/?utm_medium=microsoft&utm_source=docs.microsoft.com&utm_campaign=button+cta&utm_content=download+vs2019+rc)(When developing)<br>


## How to Install
1. install [Python 3.7.6](https://www.python.org/downloads/release/python-376/) or higher<br>
2. install **reversi**(run the following)
```
$ py -3.7 -m pip install git+https://github.com/y-tetsu/reversi
```

## How to Uninstall
uninstall **reversi**(run the following)
```
$ py -3.7 -m pip uninstall reversi
```

## Examples
Run the following in any folder to copy the examples.
```
$ install_reversi_examples
```

The examples to be copied are below.

- [01_tkinter_app.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/01_tkinter_app.py) - GUI Reversi Application(using tkinter)
- [02_console_app.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/02_console_app.py) - Console Reversi Application
- [03_create_exe.bat](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/03_create_exe.bat) - A example for creating portable GUI Reversi Application file
- [04_reversi_simulator.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/04_reversi_simulator.py) - A battle simulator that displays the results of playing Reversi AI against each other
- [05_easy_strategy.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/05_easy_strategy.py) - A example of Reversi easy AI strategy
- [06_table_strategy.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/06_table_strategy.py) - A example of Reversi table AI strategy
- [07_minmax_strategy.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/07_minmax_strategy.py) - A example of Reversi minmax  strategy
- [08_alphabeta_strategy.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/08_alphabeta_strategy.py) - A example of Reversi alpha beta AI strategy
- [09_genetic_algorithm.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/09_genetic_algorithm.py) - A example for discovering the parameters of a reversi strategy using a genetic algorithm
- [10_x_elucidator.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/10_x_elucidator.py) - Analysis tool for deformation boards


You can run examples below.
```
$ cd reversi_examples
$ py -3.7 01_tkinter_app.py
$ py -3.7 02_console_app.py
$ 03_create_exe.bat
$ py -3.7 04_reversi_simulator.py
$ py -3.7 05_easy_strategy.py
$ py -3.7 06_table_strategy.py
$ py -3.7 07_minmax_strategy.py
$ py -3.7 08_alphabeta_strategy.py
$ py -3.7 09_genetic_algorithm.py
$ py -3.7 10_x_elucidator.py
```

## How to use the library
### Basics
This section explains the basic usage of this library based on coding examples.

#### Launching an application
First, we will show how to launch a reversi GUI application.

Execute the following code.
```Python
from reversi import Reversi

Reversi().start()
```
The application will start and you can play with two players as it is.<br>
(In this case, the only player that can be selected is the user operation)<br>

#### Adding an AI to your application
Next, we show how to add an AI to your application.

As an example, we add the following AI, which is pre-loaded in the library, to your application.
- AI that plays random moves : `Random`.
- AI that plays moves to get as many stones as possible :`Greedy`.

```Python
from reversi import Reversi
from reversi.strategies import Random, Greedy

Reversi(
    {
        'RANDOM': Random(),
        'GREEDY': Greedy(),
    }
).start()
```
After the above is done, "RANDOM" and "GREEDY" can be selected as the player in addition to the user operation.

All built-in AIs can be imported from `reversi.strategies`.<br>
For more information on other available AIs, please refer to [AI class](#AI-class).<br>
The player information to be added (hereinafter referred to as "player information") should follow the format below.<br>
Player names can be set arbitrarily.<br>
```Python
{
    'PlayerName1': AI-Object1,
    'PlayerName2': AI-Object2,
    'PlayerName3': AI-Object3,
}
```

#### Programming an AI
The following shows how to use this library to create your own AI and add it to your application.

##### How to create an AI class
Coding as follows will complete the AI class.
```Python
from reversi.strategies import AbstractStrategy

class OriginalAI(AbstractStrategy):
    def next_move(self, color, board):
        #
        # Please code the logic to determine the next move (X, Y).
        #

        return (X, Y)
```
The `next_move` method implements logic to return where to place a stone (the next move) at a particular move number and board level. <br>
See below for the arguments of the `next_move` method.
 |Arguments|Description|
 |:---|:---|
 |`color` variable|`black` or `white` string of type `str` is passed to determine whether the number is black or white, respectively. |
 |`board` object| object containing information about the reversi board. The object contains parameters and methods necessary for the game to progress, such as the placement of black and white stones, and the acquisition of the positions where stones can be placed. |

Note that the (X, Y) coordinates of the return value are the values when the upper left corner of the board is set to (0, 0).<br>
The following figure shows the coordinates of each square when the board size is 8.

![coordinate](https://raw.githubusercontent.com/y-tetsu/reversi/images/coordinate.png)

As for the `board` object, for simplicity, we will focus on two of them: the `get_legal_moves` method to get the position where a stone can be placed, and the `size` parameter to get the size of the board.
For a more detailed explanation, please refer to [How to use the board object](#How-to-use-the-board-object).

##### How to get the positions where stones can be placed
You can get the positions (coordinates) where stones can be placed on a board by using the `get_legal_moves` method of the `board` object.<br>
When calling `get_legal_moves`, give either the black or white move number (`color` variable) as an argument.

```Python
legal_moves = board.get_legal_moves(color)
```

The return value of `get_legal_moves` is "a list of coordinates where stones can be placed".

The result of the black move with the initial state (board size 8) is as follows.

```
[(3, 2), (2, 3), (5, 4), (4, 5)]
```

##### Board Size
This application is designed to allow an even number of board sizes from 4 to 26 to be selected.
If necessary, please consider the size of the board so that it will work in either case.

The size of the board can be obtained by the following description.

```Python
size = board.size
```

##### Implementing the "Always take a corner when you can" AI
The following is an example of creating an AI named `Corner` that always takes 4 corners when it can, and makes random moves when it cannot(The player name is "CORNER").

```Python
import random

from reversi import Reversi
from reversi.strategies import AbstractStrategy

class Corner(AbstractStrategy):
    def next_move(self, color, board):
        size = board.size
        legal_moves = board.get_legal_moves(color)
        for corner in [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)]:
            if corner in legal_moves:
                return corner

        return random.choice(legal_moves)

Reversi({'CORNER': Corner()}).start()
```

After the above is done, "CORNER" can be selected as a player to play against.<br>
If you actually play against a player, you will see that he will always take the corner when he can!


#### Simulate a match between AIs
The simulator in this library can be used to play AIs against each other multiple times to produce a winning percentage.<br>
Use it to measure the strength of your own AI.<br>
If the AI's moves are fixed for a particular board, you can reduce the bias of the results by setting the random_opening parameter described separately below.

As an example of running the simulator The following is an example of running the simulator, showing the "RANDOM," "GREEDY," and "CORNER" games that have appeared so far in a round-robin competition, up to the display of the results.

##### Running the Simulator
Execute the following to start the simulation.
```Python
from reversi import Simulator

if __name__ == '__main__':
    simulator = Simulator(
        {
            'RANDOM': Random(),
            'GREEDY': Greedy(),
            'CORNER': Corner(),
        },
        './simulator_setting.json',
    )
    simulator.start()
```
The simulator must be executed in the main module (\_\_main\_\_).<br>
The simulator argument should be "player information" and "simulator configuration file".

##### Simulator Configuration File
An example of creating a simulator configuration file (JSON format) is shown below.
Specify the name of this file (in the above example, `. /simulator_setting.json` in the above example, but it is optional.

```JSON
{
    "board_size": 8,
    "board_type": "bitboard",
    "matches": 100,
    "processes": 1,
    "parallel": "player",
    "random_opening": 0,
    "player_names": [
        "RANDOM",
        "GREEDY",
        "CORNER"
    ]
}
```

 |parameter name|description|
 |:---|:---|
 |board_size|Specify the size of the board. |
 |board_type|Select board type (board or bitboard). bitboard is faster and should usually be used. |
 |matches|Specify the number of games played between AIs. 100 means 100 games for each combination of AIs, one for the first move and one for the second move. |
 |processes|Specify the number of parallel runs. The larger the setting, the faster the simulation results may be obtained, depending on the number of cores in your PC. |
 |parallel|Specify the unit of parallel execution. If you specify "player" (default), parallel processing is performed for each combination of AI matches. If "game" is specified, the number of matches in "matches" is divided by the number of processes and parallel processing is performed. If the number of AI matchups to be simulated is smaller than the number of cores in your PC, you may get faster results by specifying "game". |
 |random_opening|From the start of the game until the specified number of moves, the AI will play random moves against each other. When the number of moves exceeds the specified number, the AI will play its original move. By randomizing the starting situation of the game, it reduces the bias of the result and makes it easier to measure the strength of the AI. If you don't need it, please specify 0. |
 |player_names|List the names of the AIs you want to play against. If specified, select one of the names included in the first argument "player information". If omitted, it is treated as the same as the first argument "player information". All listed AIs compete against each other in a round-robin game. |


##### Execution Result
The simulation results can be seen in the printout below after the simulation is run (after the start method is executed).
```Python
print(simulator)
```

##### Running example
Run the simulator against players "RANDOM" and "GREEDY" using the library's built-in AI, and "CORNER" using our own AI. and "CORNER" using our own AI, respectively, and outputs the results. The following is an example of the code to run the simulator and output the results.

```Python
import random

from reversi import Simulator
from reversi.strategies import AbstractStrategy, Random, Greedy

class Corner(AbstractStrategy):
    def next_move(self, color, board):
        size = board.size
        legal_moves = board.get_legal_moves(color)
        for corner in [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)]:
            if corner in legal_moves:
                return corner

        return random.choice(legal_moves)

if __name__ == '__main__':
    simulator = Simulator(
        {
            'RANDOM': Random(),
            'GREEDY': Greedy(),
            'CORNER': Corner(),
        },
        './simulator_setting.json',
    )
    simulator.start()

    print(simulator)
```

The following results were obtained after 100 rounds of "RANDOM," "GREEDY," and "CORNER" games, played first and second hand, respectively.

```
Size : 8
                          | RANDOM                    GREEDY                    CORNER
---------------------------------------------------------------------------------------------------------
RANDOM                    | ------                     32.5%                     21.5%
GREEDY                    |  66.0%                    ------                     29.5%
CORNER                    |  76.0%                     68.5%                    ------
---------------------------------------------------------------------------------------------------------

                          | Total  | Win   Lose  Draw  Match
------------------------------------------------------------
RANDOM                    |  27.0% |   108   284     8   400
GREEDY                    |  47.8% |   191   202     7   400
CORNER                    |  72.2% |   289   102     9   400
------------------------------------------------------------
```

The results show that it seems to be more advantageous to take more each time than to hit randomly, and even more so to always take a corner.

### Objects
This section describes the various objects provided in this library.

#### How to use board object
This section describes how to use the `board` object, which manages the reversi board.

##### Creating a board object
A `board` object can be created by importing the `Board` or `BitBoard` class from **reversi**.
Import the `Board` or `BitBoard` class from **reversi** to create a `board` object.

The only difference between the `Board` and `BitBoard` classes is the structure of the internal data representing the board, and their usage is the same.
Since the `BitBoard` class is faster, you should usually use this class.

When instantiating the `BitBoard` class, you can specify the size of the board by entering a numerical value as an argument.
The size should be an even number from 4 to 26. If omitted, the size is 8.
You can also check the size of the board with the `size` property.

A coding example is shown below.

```Python
from reversi import Board, BitBoard

board = Board()
print(board.size)

bitboard = BitBoard(10)
print(bitboard.size)
```

The results of the above execution are as follows.
```
8
10
```

##### Standard output of a board object
When you `print` a `board` object, the state of the board is printed as standard output.

```Python
from reversi import BitBoard

board = BitBoard()
print(board)

board = BitBoard(4)
print(board)
```

The results of the above execution are as follows.<br>
![board_print](https://raw.githubusercontent.com/y-tetsu/reversi/images/board_print.png)

##### Methods of the `board` object
Here are the available methods of the `board` object.

###### get_legal_moves
Returns the possible move positions for the black or white board.
The possible moves are a "list of tuples of XY coordinates".
The argument must be a `black` or `white` string (hereafter called `color`).

```Python
from reversi import BitBoard

board = BitBoard()
legal_moves = board.get_legal_moves('black')

print(legal_moves)
```

The results of the above execution are as follows.
```
[(3, 2), (2, 3), (5, 4), (4, 5)]
```

In this case, the position of the yellow square in the figure below is returned as the possible starting position.<br>
![legal_moves](https://raw.githubusercontent.com/y-tetsu/reversi/images/legal_moves.png)

###### get_flippable_discs
Returns the stones that can be flipped if the move is made at the specified position.
The flippable stones are "a list of tuples of XY coordinates".
The first argument is the `color`, the second is the X coordinate at which to place the stone, and the third is the Y coordinate.

```Python
from reversi import BitBoard

board = BitBoard()
flippable_discs = board.get_flippable_discs('black', 5, 4)

print(flippable_discs)
```

The results of the above execution are as follows.
```
[(4, 4)]
```

In this case, the position of the yellow square in the diagram below is returned as the position of the stone that can be turned over.<br>
![flippable_discs](https://raw.githubusercontent.com/y-tetsu/reversi/images/flippable_discs2.png)

###### get_board_info
Returns a "two-dimensional list" of stones on the board.
1" means black, "-1" means white, and "0" means empty. There is no argument.


```Python
from pprint import pprint
from reversi import BitBoard

board = BitBoard()
board_info = board.get_board_info()

print(board)
pprint(board_info)
```

The results of the above execution are as follows.
![get_board_info](https://raw.githubusercontent.com/y-tetsu/reversi/images/get_board_info.png)

###### get_board_line_info
Returns information about the board as a one-line string.

```Python
from pprint import pprint
from reversi import BitBoard

board = BitBoard()

print(board.get_board_line_info('black'))
```

The results of the above execution are as follows.
```
---------------------------O*------*O---------------------------*
```

The format is: board square information + player information.

The argument must be a string ('black' or 'white') indicating the player.

The default character assignments are as follows
- "*" : black player
- "O" : white player
- "-" : empty square

You can change it to a character of your choice by specifying an optional argument.
```Python
print(board.get_board_line_info(player='black', black='0', white='1', empty='.'))
```

The above execution produces the following output.
```
...........................10......01...........................0
```

- player : Please specify 'black' or 'white'.
- black : Specify the character to be assigned to black
- white : Specify the character to be assigned to the white square.
- empty : Specify the character to be assigned to the empty square

###### put_disc
Places a stone at the specified position and turns over the stone to be taken.
Specify `color` as the first argument, X coordinate to place the stone as the second argument, and Y coordinate as the third argument.

```Python
from reversi import BitBoard

board = BitBoard()
print(board)

board.put_disc('black', 5, 4)
print(board)
```

The above execution produces the following output.<br>
![put_disc](https://raw.githubusercontent.com/y-tetsu/reversi/images/put_disc.png)

###### undo
Undo a stone placed by the `put_disc` method. There is no argument.
You can undo as many times as you call the `put_disc` method.
Do not call this method more times than you called the `put_disc` method.

```Python
from reversi import BitBoard

board = BitBoard()
board.put_disc('black', 5, 4)
print(board)

board.undo()
print(board)
```

The above execution produces the following output.<br>
![undo](https://raw.githubusercontent.com/y-tetsu/reversi/images/undo.png)

#### How to use color object
So far, we have shown how to use the string `black' or `white' to determine the black or white move number, but it is also possible to specify the black or white move number using a `color` object.

You can import a `color` object, `C`, as shown below, and specify the black and white numbers with the black and white properties, respectively.

```Python
from reversi import BitBoard
from reversi import C as c

board = BitBoard()
board.put_disc(c.black, 5, 4)
print(board)

board.put_disc(c.white, 5, 5)
print(board)
```

The above execution produces the following output.<br>
![color](https://raw.githubusercontent.com/y-tetsu/reversi/images/color.png)

#### How to use move object
The `move` object allows you to specify the coordinates of a move not only in XY coordinate format, but also in str format, such as 'a1', 'c3', etc. The str format allows both upper and lower case alphabets.

Import the `Move` class and use it as follows.
```Python
from reversi import BitBoard
from reversi import C as c
from reversi import Move as m

board = BitBoard()
board.put_disc(c.black, *m('f5'))
print(board)

board.put_disc(c.white, *m('f6'))
print(board)
```

The above execution produces the following output.<br>
![color](https://raw.githubusercontent.com/y-tetsu/reversi/images/color.png)

Also, a A `move` object can also be generated in XY coordinate format and converted to str format using the str function. If you print a `move` object, it will be in str format as well, and if you specify `upper` as the case option, it will be in upper case.

```Python
from reversi import BitBoard
from reversi import Move as m

move = str(m(5, 4))
print(move)
print(m(5, 5, case='upper'))
```

The above execution produces the following output.<br>
```
f5
F6
```

---
## Footnotes
<a id="note1">[1]</a>: Cython is used in some parts.<sup>[↑](#return1)</sup>


---
## License
The source code of this repository is [MIT License](http://www.opensource.org/licenses/MIT).
Please feel free to use it for both commercial and non-commercial purposes.
