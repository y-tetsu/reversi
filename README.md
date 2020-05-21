# reversi
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
<br>
[ [English](https://github.com/y-tetsu/reversi/blob/master/README.md) | [日本語](https://github.com/y-tetsu/reversi/blob/master/README.ja.md)]<br>

## Introduction
This is a reversi library for Python.<br>

You can easily program and play Reversi (Othello) AI.
![gui](https://github.com/y-tetsu/reversi/blob/master/image/reversi_en.gif?raw=true)

For Windows OS, you can download the executable application from the following.<br>
[Download](https://github.com/y-tetsu/reversi/releases)

## Requirement
- Windows10 64bit<br>
- Display size 1366x768
- Processe 1.6GHz
- Memory 4.00GB
- [Python 3.7.6](https://www.python.org/downloads/release/python-376/)<br>
    - cython 0.29.15<br>
    - numpy 1.18.1<br>
    - pyinstaller 3.6<br>
- [Microsoft Visual C++ 2019](https://visualstudio.microsoft.com/downloads/?utm_medium=microsoft&utm_source=docs.microsoft.com&utm_campaign=button+cta&utm_content=download+vs2019+rc)<br>

## How to Install
### Windows
1. install [Python 3.7.6 or higher](https://www.python.org/downloads/release/python-376/)<br>
2. install [Microsoft Visual C++ 2019](https://visualstudio.microsoft.com/downloads/?utm_medium=microsoft&utm_source=docs.microsoft.com&utm_campaign=button+cta&utm_content=download+vs2019+rc)<br>
3. update pip command(run the following)
```
$ py -3.7 -m pip install --upgrade pip
```
4. install **reversi**(run the following)
```
$ py -3.7 -m pip install git+https://github.com/y-tetsu/reversi
```

### Install examples
Execute the following in any folder to copy the examples.
```
$ install_reversi_examples
```

The examples to be copied are below.

- [01_gui_app.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/01_gui_app.py) - GUI Application
- [02_console_app.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/02_console_app.py) - Console Application
- [03_strategy_customization.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/03_strategy_customization.py) - Base script for programming Reversi AI strategy
- [04_reversi_simulator.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/04_reversi_simulator.py) - A battle simulator that displays the results of playing Reversi AI against each other
- [05_genetic_algorithm.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/05_genetic_algorithm.py) - A example for discovering the parameters of a reversal strategy using a genetic algorithm

You can run the sample below.

#### Windows
```
$ cd reversi_examples
$ py -3.7 01_gui_app.py
```
