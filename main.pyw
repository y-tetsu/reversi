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


class Main:
    """
    GUIゲーム
    """
    INIT, DEMO, PLAY, END, REINIT = 'INIT', 'DEMO', 'PLAY', 'END', 'REINIT'

    def __init__(self, window=None, strategies=None):
        self.state = Main.INIT
        self.window = window
        self.strategies = strategies

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

        if state == Main.INIT:
            self.game = self.__init
        elif state == Main.DEMO:
            self.game = self.__demo
        elif state == Main.PLAY:
            self.game = self.__play
        elif state == Main.END:
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

        self.state = Main.DEMO

    def __demo(self):
        """
        デモ画面
        """
        while True:
            time.sleep(0.1)

            if self.window.start_pressed:
                window.start_pressed = False
                self.state = Main.PLAY
                break

            if self._setting_changed():
                self.state = Main.INIT
                break

    def __play(self):
        """
        ゲーム画面
        """
        # ボード準備
        board = Board(self.window.size)

        # プレイヤー準備
        black = Player(board.black, self.window.player['black'], self.strategies[self.window.player['black']])
        white = Player(board.white, self.window.player['white'], self.strategies[self.window.player['white']])

        # ゲーム開始
        game = Game(board, black, white, WindowDisplay(self.window))
        game.play()

        # 少し待って終了状態へ
        time.sleep(2)
        self.state = Main.END

    def __end(self):
        """
        終了画面
        """
        window.enable_window()

        while True:
            time.sleep(0.1)

            if window.start_pressed:
                window.start_pressed = False
                self.state = Main.REINIT
                break

            if self._setting_changed():
                self.state = Main.INIT
                break

    def __reinit(self):
        """
        再初期化(ゲーム終了後再スタート時)
        """
        window.init_game_screen()
        window.disable_start()
        window.menubar.disable_menu()
        self.state = Main.PLAY

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
    window = Window(root=root, event=event, queue=q)

    # ゲーム戦略
    game_strategies = {
        'User1': strategies.WindowUserInput(window),
        'User2': strategies.WindowUserInput(window),
        'Unselfish': strategies.Unselfish(),
        'Random': strategies.Random(),
        'Greedy': strategies.Greedy(),
    }

    # ゲーム用スレッド
    main = Main(window=window, strategies=game_strategies)
    game = threading.Thread(target=main.mainloop)
    game.daemon = True
    game.start()

    # GUI用スレッド
    root.deiconify()  # 表示する
    root.mainloop()
