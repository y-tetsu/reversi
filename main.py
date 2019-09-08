#!/usr/bin/env python
"""
オセロアプリ(コンソール版)
"""

import sys
import time

import board
from board import Board
from player import Player
from display import ConsoleDisplay
from game import Game
import strategies


BLACK_PLAYERS = {
    'User1': strategies.ConsoleUserInput(),
    'Random': strategies.Random(),
    'Greedy': strategies.Greedy(),
    'Unselfish': strategies.Unselfish(),
}

WHITE_PLAYERS = {
    'User2': strategies.ConsoleUserInput(),
    'Random': strategies.Random(),
    'Greedy': strategies.Greedy(),
    'Unselfish': strategies.Unselfish(),
}

DEFAULT_BLACK_PLAYER = 'User1'
DEFAULT_WHITE_PLAYER = 'Random'
DEFAULT_BOARD_SIZE = 4


class Main:
    """
    コンソールゲーム
    """
    START, MENU, PLAY = 'START', 'MENU', 'PLAY'

    def __init__(self):
        self.board_size = DEFAULT_BOARD_SIZE
        self.black = DEFAULT_BLACK_PLAYER
        self.white = DEFAULT_WHITE_PLAYER
        self.state = Main.START

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

        if state == Main.START:
            self.game = self.__start
        elif state == Main.MENU:
            self.game = self.__menu
        else:
            self.game = self.__play

    def mainloop(self):
        """
        メインループ
        """
        while True:
            self.game()

    def __start(self):
        """
        設定を表示
        """
        print('\n=============================')
        print('BoardSize   =', self.board_size)
        print('BlackPlayer =', self.black)
        print('WhitePlayer =', self.white)
        print('=============================\n')
        self.state = Main.MENU

    def __menu(self):
        """
        メニュー
        """
        print('press any key')
        print('-----------------------------')
        print(' enter  : start game')
        print(' s      : change board size')
        print(' b      : change black player')
        print(' w      : change white player')
        print(' q      : quit')
        print('-----------------------------')

        while True:
            user_in = input('>> ')

            if not user_in:
                self.state = Main.PLAY
                break
            elif user_in == 's':
                self.board_size = self._get_board_size()
                self.state = Main.START
                break
            elif user_in == 'b':
                self.black = self._get_player(BLACK_PLAYERS)
                self.state = Main.START
                break
            elif user_in == 'w':
                self.white = self._get_player(WHITE_PLAYERS)
                self.state = Main.START
                break
            elif user_in == 'q':
                print('See you!')
                sys.exit()

    def _get_board_size(self):
        """
        ボードサイズの取得
        """
        print('press board size')

        while True:
            user_in = int(input('>> '))

            if board.MIN_BOARD_SIZE <= user_in <= board.MAX_BOARD_SIZE and not user_in % 2:
                return user_in

    def _get_player(self, players):
        """
        プレイヤーの取得
        """
        player_list = list(players.keys())

        print('select number for player')
        print('-----------------------------')
        for num, value in enumerate(player_list, 1):
            print(f' {num:2d} : {value}')
        print('-----------------------------')

        while True:
            user_in = int(input('>> '))

            if 1 <= user_in <= len(player_list):
                return player_list[user_in-1]

    def __play(self):
        """
        ゲームプレイ
        """
        # プレイヤー準備
        black = Player(Board.BLACK, self.black, BLACK_PLAYERS[self.black])
        white = Player(Board.WHITE, self.white, WHITE_PLAYERS[self.white])

        # ゲーム開始
        game = Game(Board(self.board_size), black, white, ConsoleDisplay())
        game.play()

        # 少し待ってスタートに戻る
        time.sleep(2)
        self.state = Main.START


if __name__ == '__main__':
    main = Main()
    main.mainloop()
