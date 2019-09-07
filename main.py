#!/usr/bin/env python
"""
オセロゲーム(コンソール版)
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
    MENU, GAME = 'MENU', 'GAME'

    def __init__(self):
        self.board_size = DEFAULT_BOARD_SIZE
        self.black = DEFAULT_BLACK_PLAYER
        self.white = DEFAULT_WHITE_PLAYER
        self.state = Main.MENU

    def show_setting(self):
        """
        設定を表示
        """
        print('\n=============================')
        print('BoardSize   =', self.board_size)
        print('BlackPlayer =', self.black)
        print('WhitePlayer =', self.white)
        print('=============================\n')

    def menu(self):
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
                self.state = Main.GAME
                break
            elif user_in == 's':
                self.board_size = self.get_board_size()
                break
            elif user_in == 'b':
                self.black = self.get_player(BLACK_PLAYERS)
                break
            elif user_in == 'w':
                self.white = self.get_player(WHITE_PLAYERS)
                break
            elif user_in == 'q':
                print('See you!')
                sys.exit()
                break

    def get_board_size(self):
        """
        ボードサイズの取得
        """
        print('press board size')

        while True:
            user_in = int(input('>> '))

            if board.MIN_BOARD_SIZE <= user_in <= board.MAX_BOARD_SIZE and not user_in % 2:
                return user_in

    def get_player(self, players):
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

    def game(self):
        """
        ゲーム
        """
        # プレイヤー準備
        black = Player(Board.BLACK, self.black, BLACK_PLAYERS[self.black])
        white = Player(Board.WHITE, self.white, WHITE_PLAYERS[self.white])

        # ゲーム開始
        game = Game(Board(self.board_size), black, white, ConsoleDisplay())
        game.play()

        # 少し待ってメニューに戻る
        time.sleep(2)
        self.state = Main.MENU


if __name__ == '__main__':
    main = Main()

    while True:
        main.show_setting()

        if main.state == Main.MENU:
            main.menu()

        if main.state == Main.GAME:
            main.game()
