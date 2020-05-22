<p align="center">
<img src="https://raw.githubusercontent.com/y-tetsu/reversi/images/tkinter_app_demo.gif" width="800px">
</p>

# reversi
[ [English](https://github.com/y-tetsu/reversi/blob/master/README.md) | [日本語](https://github.com/y-tetsu/reversi/blob/master/README.ja.md)]<br>
<br>
This is a reversi library for Python.<br>
You can feel free to enjoy programming Reversi (Othello) AI.<br>
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
<br>

## Download
For Windows OS, you can download the Reversi Application(using tkinter) from the following.<br>
[Download Reversi Application](https://github.com/y-tetsu/reversi/releases)

## Requirement
- Windows10 64bit<br>
- Display size 1366x768
- Processor 1.6GHz
- Memory 4.00GB
- [Python 3.7.6](https://www.python.org/downloads/release/python-376/)<br>
    - cython 0.29.15<br>
    - numpy 1.18.1<br>
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
- [03_strategy_customization.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/03_strategy_customization.py) - Base script for programming Reversi AI strategy
- [04_reversi_simulator.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/04_reversi_simulator.py) - A battle simulator that displays the results of playing Reversi AI against each other
- [05_genetic_algorithm.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/05_genetic_algorithm.py) - A example for discovering the parameters of a reversi strategy using a genetic algorithm
- [06_create_exe.bat](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/06_create_exe.bat) - A example for creating portable GUI Reversi Application file

You can run examples below.
```
$ cd reversi_examples
$ py -3.7 01_tkinter_app.py
$ py -3.7 02_console_app.py
$ py -3.7 03_strategy_customization.py
$ py -3.7 04_reversi_simulator.py
$ py -3.7 05_genetic_algorithm.py
$ 06_create_exe.bat
```

### Deomo
[<img src="https://raw.githubusercontent.com/y-tetsu/reversi/images/tkinter_app_demo.gif" width="500">](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/01_tkinter_app.py)
[<img src="https://raw.githubusercontent.com/y-tetsu/reversi/images/console_app_demo.gif" width="500">](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/02_console_app.py)
[<img src="https://raw.githubusercontent.com/y-tetsu/reversi/images/simulator_demo.gif" width="500">](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/04_reversi_simulator.py)

