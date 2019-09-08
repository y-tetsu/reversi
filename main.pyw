#!/usr/bin/env python
"""
オセロアプリ(GUI版)
"""

import sys
import time

import board
from board import Board
from player import Player
from display import WindowDisplay
from game import Game
import strategies


BLACK_PLAYERS = {
    'User1': strategies.WindowUserInput(),
    'Random': strategies.Random(),
    'Greedy': strategies.Greedy(),
    'Unselfish': strategies.Unselfish(),
}

WHITE_PLAYERS = {
    'User2': strategies.WindowUserInput(),
    'Random': strategies.Random(),
    'Greedy': strategies.Greedy(),
    'Unselfish': strategies.Unselfish(),
}

DEFAULT_BOARD_SIZE = 4


class Main:
    """
    GUIゲーム
    """
    INIT, DEMO, PLAY, END, REINIT = 'INIT', 'DEMO', 'PLAY', 'END', 'REINIT'

    def __init__(self, window=None):
        self.state = Main.INIT
        self.window = window

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
        print('INIT')

        self.window.init_game_screen()
        self.window.enable_window()

        self.state = Main.DEMO

    def __demo(self):
        """
        デモ画面
        """
        print('DEMO')

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
        print('PLAY')

        # プレイヤー準備
        black = Player(Board.BLACK, self.window.black_player, BLACK_PLAYERS[self.window.black_player])
        white = Player(Board.WHITE, self.window.white_player, WHITE_PLAYERS[self.window.white_player])

        # ゲーム開始
        game = Game(Board(self.window.size), black, white, WindowDisplay(self.window))
        game.play()

        # 少し待って終了状態へ
        time.sleep(2)
        self.state = Main.END

    def __end(self):
        """
        終了画面
        """
        print('END')

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
        print('REINIT')

        window.init_game_screen()
        window.disable_start()
        window.menubar.disable_menu()
        self.state = Main.PLAY

    def _setting_changed(self):
        """
        ウィンドウの設定が変更されたとき
        """
        if self.window.event.is_set():
            self.window.size = self.window.queue.get()
            self.window.event.clear()

            return True

        return False


if __name__ == '__main__':
    import threading
    import queue
    import tkinter as tk

    from window import Window

    event = threading.Event()
    q = queue.Queue()

    # ウィンドウ作成
    app = tk.Tk()
    app.withdraw()  # 表示が整うまで隠す
    window = Window(size=DEFAULT_BOARD_SIZE, master=app, event=event, queue=q)

    # ゲーム用スレッド
    main = Main(window=window)
    game = threading.Thread(target=main.mainloop)
    game.daemon = True
    game.start()

    # GUI用スレッド
    app.deiconify()  # 表示する
    app.mainloop()
