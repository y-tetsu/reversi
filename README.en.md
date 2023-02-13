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
        - [Adding AI to your application](#Adding-AI-to-your-application)
        - [Programming AI](#Programming-AI)
        - [Simulate a match between AIs](#Simulate-a-match-between-AIs)
    - [Objects](#Objects)
        - [How to use board object](#How-to-use-board-object)
        - [How to use color object](#How-to-use-board-object)
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


## System Requirement
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

---
## Footnotes
<a id="note1">[1]</a>: Cython is used in some parts.<sup>[↑](#return1)</sup>


---
## License
The source code of this repository is [MIT License](http://www.opensource.org/licenses/MIT).
Please feel free to use it for both commercial and non-commercial purposes.
