#!/usr/bin/env python
"""
GUI版リバーシアプリ
"""

if '__file__' in globals():
    import os, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import threading
import tkinter as tk

from reversi import Reversi, Window, strategies

# ウィンドウ作成
root = tk.Tk()
root.withdraw()  # 表示が整うまで隠す

b = ['User1', 'Unselfish', 'Random', 'Greedy', 'SlowStarter', 'Table', 'MonteCarlo', 'MinMax', 'NegaMax', 'AlphaBeta', 'Joseki', 'FullReading', 'Iterative', 'Edge']
w = ['User2', 'Unselfish', 'Random', 'Greedy', 'SlowStarter', 'Table', 'MonteCarlo', 'MinMax', 'NegaMax', 'AlphaBeta', 'Joseki', 'FullReading', 'Iterative', 'Edge']

w = Window(root=root, black_players=b, white_players=w)

# ゲーム戦略
s = {
    'User1': strategies.WindowUserInput(w),
    'User2': strategies.WindowUserInput(w),
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

# ゲーム用スレッド
reversi = Reversi(window=w, strategies=s)
game = threading.Thread(target=reversi.mainloop)
game.daemon = True
game.start()

# GUI用スレッド
root.deiconify()  # 表示する
root.mainloop()
