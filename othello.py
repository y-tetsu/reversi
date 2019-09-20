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


TURN_STONE_WAIT = 0.1


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
        self.window.set_state('normal')
        self.state = Othello.DEMO

    def __demo(self):
        """
        デモ画面
        """
        while True:
            if self.window.start.event.is_set():
                self.window.set_state('disable')
                self.window.start.event.clear()
                self.state = Othello.PLAY
                break

            if not self._demo_animation():
                self.state = Othello.INIT
                break

    def _demo_animation(self):
        """
        デモアニメーション継続中
        """
        center = self.window.board.size // 2
        target = [
            ('black', center, center-1),
            ('black', center-1, center),
            ('white', center-1, center-1),
            ('white', center, center),
        ]
        ptn = {
            'black': [
                ('black', self.window.board.put_turnblack),
                ('turnblack', self.window.board.put_white),
                ('white', self.window.board.put_turnwhite),
                ('turnwhite', self.window.board.put_black),
            ],
            'white': [
                ('white', self.window.board.put_turnwhite),
                ('turnwhite', self.window.board.put_black),
                ('black', self.window.board.put_turnblack),
                ('turnblack', self.window.board.put_white),
            ],
        }

        for color, x, y in target:
            for remove_color, put_stone in ptn[color]:
                # メニュー設定変更時
                if self._setting_changed():
                    return False

                # アニメーション処理
                time.sleep(TURN_STONE_WAIT)
                self.window.board.remove_stone(remove_color, x, y)
                put_stone(x, y)

        return True

    def __play(self):
        """
        ゲーム画面
        """
        # ボード準備
        board = Board(self.window.board.size)

        # プレイヤー準備
        players = {}

        for color in ('black', 'white'):
            name = self.window.player[color]
            players[color] = Player(color, name, self.strategies[name])

        # ゲーム開始
        game = Game(board, players['black'], players['white'], WindowDisplay(self.window))
        game.play()

        # 少し待って終了状態へ
        time.sleep(1.5)
        self.state = Othello.END

    def __end(self):
        """
        終了画面
        """
        self.window.set_state('normal')

        while True:
            time.sleep(0.01)

            if self.window.start.event.is_set():
                self.window.menu.set_state('disable')
                self.window.start.event.clear()
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
        self.window.set_state('disable')
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
    import tkinter as tk

    # ウィンドウ作成
    root = tk.Tk()
    root.withdraw()  # 表示が整うまで隠す

    b = ['User1', 'Unselfish', 'Random', 'Greedy']
    w = ['User2', 'Unselfish', 'Random', 'Greedy']

    w = Window(root=root, black_players=b, white_players=w)

    # ゲーム戦略
    s = {
        'User1': strategies.WindowUserInput(w),
        'User2': strategies.WindowUserInput(w),
        'Unselfish': strategies.Unselfish(),
        'Random': strategies.Random(),
        'Greedy': strategies.Greedy(),
    }

    # ゲーム用スレッド
    othello = Othello(window=w, strategies=s)
    game = threading.Thread(target=othello.mainloop)
    game.daemon = True
    game.start()

    # GUI用スレッド
    root.deiconify()  # 表示する
    root.mainloop()
