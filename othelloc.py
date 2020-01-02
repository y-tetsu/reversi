#!/usr/bin/env python
"""
オセロアプリ(コンソール版)
"""

import sys
import time

import board
from board import BitBoard
from player import Player
from display import ConsoleDisplay
from game import Game
import strategies


BLACK_STRATEGIES = {
    'User1': strategies.ConsoleUserInput(),
    'Unselfish': strategies.Unselfish(),
    'Random': strategies.Random(),
    'Greedy': strategies.Greedy(),
    'SlowStarter': strategies.SlowStarter(),
    'Table': strategies.Table(),
    'MinMax': strategies.MinMax2_TPW(),
    'MonteCarlo': strategies.MonteCarlo1000(),
    'NegaMax': strategies.NegaMax3_TPW(),
    'AlphaBeta': strategies.AlphaBeta4_TPW(),
    'AB_T': strategies.AB_T4(),
    'AB_TI': strategies.AB_TI(),
    'AbIF11_B_TPW': strategies.AbIF11_B_TPW(),
}

WHITE_STRATEGIES = {
    'User2': strategies.ConsoleUserInput(),
    'Unselfish': strategies.Unselfish(),
    'Random': strategies.Random(),
    'Greedy': strategies.Greedy(),
    'Table': strategies.Table(),
    'MinMax': strategies.MinMax2_TPW(),
    'MonteCarlo': strategies.MonteCarlo1000(),
    'NegaMax': strategies.NegaMax3_TPW(),
    'AlphaBeta': strategies.AlphaBeta4_TPW(),
    'AB_T': strategies.AB_T4(),
    'AB_TI': strategies.AB_TI(),
    'AbIF11_B_TPW': strategies.AbIF11_B_TPW(),
}

STRATEGIES = {'black': BLACK_STRATEGIES, 'white': WHITE_STRATEGIES}

DEFAULT_BLACK_PLAYER = 'User1'
DEFAULT_WHITE_PLAYER = 'Random'
DEFAULT_BOARD_SIZE = 4


class Othelloc:
    """
    コンソールゲーム
    """
    START, MENU, PLAY = 'START', 'MENU', 'PLAY'

    def __init__(self):
        self.board_size = DEFAULT_BOARD_SIZE
        self.player_names = {'black': DEFAULT_BLACK_PLAYER, 'white': DEFAULT_WHITE_PLAYER}
        self.state = Othelloc.START

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

        if state == Othelloc.START:
            self.game = self.__start
        elif state == Othelloc.MENU:
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
        print('BlackPlayer =', self.player_names['black'])
        print('WhitePlayer =', self.player_names['white'])
        print('=============================\n')
        self.state = Othelloc.MENU

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
                self.state = Othelloc.PLAY
                break
            elif user_in == 's':
                self.board_size = self._get_board_size()
                self.state = Othelloc.START
                break
            elif user_in == 'b':
                self.player_names['black'] = self._get_player(BLACK_STRATEGIES)
                self.state = Othelloc.START
                break
            elif user_in == 'w':
                self.player_names['white'] = self._get_player(WHITE_STRATEGIES)
                self.state = Othelloc.START
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
        # ボード準備
        board = BitBoard(self.board_size)

        # プレイヤー準備
        selected_players = {}

        for color in ('black', 'white'):
            name = self.player_names[color]
            selected_players[color] = Player(color, name, STRATEGIES[color][name])

        # ゲーム開始
        game = Game(board, selected_players['black'], selected_players['white'], ConsoleDisplay())
        game.play()

        # 少し待ってスタートに戻る
        time.sleep(2)
        self.state = Othelloc.START


if __name__ == '__main__':
    othelloc = Othelloc()
    othelloc.mainloop()
