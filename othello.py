#!/usr/bin/env python
"""
オセロアプリ(GUI版)
"""

import sys
import time

from board import Board
from player import Player
from display import WindowDisplay
from game import Game
from window import Window
import strategies


class Othello:
    """
    GUIゲーム
    """
    INIT, DEMO, PLAY, END, REINIT = 'INIT', 'DEMO', 'PLAY', 'END', 'REINIT'

    def __init__(self, window=None, strategies=None):
        self.state = Othello.INIT
        self.window = window
        self.strategies = strategies

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

        if state == Othello.INIT:
            self.game = self.__init
        elif state == Othello.DEMO:
            self.game = self.__demo
        elif state == Othello.PLAY:
            self.game = self.__play
        elif state == Othello.END:
            self.game = self.__end
        else:
            self.game = self.__reinit

    def mainloop(self):
        """
        メインループ
        """
        while True:
            self.game()

    def __init(self):
        """
        画面初期化(初回、設定変更時)
        """
        self.window.init_screen()
        self.window.enable_window()

        self.state = Othello.DEMO

    def __demo(self):
        """
        デモ画面
        """
        while True:
            time.sleep(0.1)

            if self.window.start_pressed:
                self.window.start_pressed = False
                self.state = Othello.PLAY
                break

            if self._setting_changed():
                self.state = Othello.INIT
                break

    def __play(self):
        """
        ゲーム画面
        """
        # ボード準備
        board = Board(self.window.size)

        # プレイヤー準備
        black_name = self.window.player['black']
        white_name = self.window.player['white']
        black_player = Player(board.black, black_name, self.strategies[black_name])
        white_player = Player(board.white, white_name, self.strategies[white_name])

        # ゲーム開始
        game = Game(board, black_player, white_player, WindowDisplay(self.window))
        game.play()

        # 少し待って終了状態へ
        time.sleep(2)
        self.state = Othello.END

    def __end(self):
        """
        終了画面
        """
        self.window.enable_window()

        while True:
            time.sleep(0.1)

            if self.window.start_pressed:
                self.window.start_pressed = False
                self.state = Othello.REINIT
                break

            if self._setting_changed():
                self.state = Othello.INIT
                break

    def __reinit(self):
        """
        再初期化(ゲーム終了後再スタート時)
        """
        self.window.init_screen()
        self.window.disable_start()
        self.window.menu.set_state('disable')
        self.state = Othello.PLAY

    def _setting_changed(self):
        """
        ウィンドウの設定が変更されたとき
        """
        if self.window.menu.event.is_set():
            self.window.size = self.window.menu.size
            self.window.player['black'] = self.window.menu.black_player
            self.window.player['white'] = self.window.menu.white_player
            self.window.menu.event.clear()

            return True

        return False


if __name__ == '__main__':
    import threading
    import queue
    import tkinter as tk

    event = threading.Event()
    q = queue.Queue()

    # ウィンドウ作成
    root = tk.Tk()
    root.withdraw()  # 表示が整うまで隠す

    b = ['ユーザ', 'かんたん', 'ふつう', 'むずかしい']
    w = ['ユーザ', 'かんたん', 'ふつう', 'むずかしい']

    w = Window(root=root, event=event, queue=q, black_players=b, white_players=w)

    # ゲーム戦略
    s = {
        'ユーザ': strategies.WindowUserInput(w),
        'かんたん': strategies.Unselfish(),
        'ふつう': strategies.Random(),
        'むずかしい': strategies.Greedy(),
    }

    # ゲーム用スレッド
    othello = Othello(window=w, strategies=s)
    game = threading.Thread(target=othello.mainloop)
    game.daemon = True
    game.start()

    # GUI用スレッド
    root.deiconify()  # 表示する
    root.mainloop()