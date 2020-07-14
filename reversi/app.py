#!/usr/bin/env python
"""
アプリケーション
"""

import sys
import os
import time
import tkinter as tk
import json
import threading

from reversi import BitBoard, MIN_BOARD_SIZE, MAX_BOARD_SIZE, Player, Window, WindowDisplay, ConsoleDisplay, Game
import reversi.strategies as s


TURN_DISC_WAIT = 0.1


class Reversi:
    """
    リバーシゲーム
    """
    INIT, DEMO, PLAY, END, REINIT = 'INIT', 'DEMO', 'PLAY', 'END', 'REINIT'

    def __init__(self, strategies={}):
        root = tk.Tk()
        root.withdraw()  # 表示が整うまで隠す

        self.state = Reversi.INIT

        b = ['User1'] + list(strategies.keys())
        w = ['User2'] + list(strategies.keys())
        self.window = Window(root=root, black_players=b, white_players=w)

        strategies['User1'] = s.WindowUserInput(self.window)
        strategies['User2'] = s.WindowUserInput(self.window)
        self.strategies = strategies

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

        if state == Reversi.INIT:
            self.game = self.__init
        elif state == Reversi.DEMO:
            self.game = self.__demo
        elif state == Reversi.PLAY:
            self.game = self.__play
        elif state == Reversi.END:
            self.game = self.__end
        else:
            self.game = self.__reinit

    def gameloop(self):
        """
        ゲーム処理
        """
        while True:
            self.game()

    def start(self):
        """
        アプリ開始
        """
        self.game_start()    # ゲーム開始
        self.window_start()  # ウィンドウ開始

    def game_start(self):
        """
        ゲーム開始
        """
        game = threading.Thread(target=self.gameloop)
        game.daemon = True
        game.start()

    def window_start(self):
        """
        ウィンドウ開始
        """
        self.window.root.deiconify()  # 表示する
        self.window.root.mainloop()

    def __init(self):
        """
        画面初期化(初回、設定変更時)
        """
        self.window.init_screen()
        self.window.set_state('normal')

        # メニューで登録ファイルが読み込まれた場合
        if self.window.extra_file:
            extra_file = self.window.extra_file
            self.window.extra_file = ""
            self._load_extra_file(extra_file)

        self.state = Reversi.DEMO

    def _load_extra_file(self, extra_file):
        """
        登録ファイルを読み込む
        """
        if os.path.isfile(extra_file):
            with open(extra_file, 'r') as f:
                try:
                    # 設定の読み出し
                    json_dict = json.load(f)
                    name = json_dict['name']
                    cmd = json_dict['cmd']
                    timeouttime = json_dict['timeouttime']

                except Exception:
                    self.error_message('フォーマットエラーのため登録ファイルが読み込めませんでした')

                # メニューにAIの名前を追加
                for color in ('black', 'white'):
                    if name not in self.window.menu.menu_items[color]:
                        self.window.menu.menu_items[color].append(name)
                        self.window.menu.menus[color].add_command(label=str(name), command=self.window.menu._command(color, name))

                # 戦略を追加
                if name not in self.strategies:
                    self.strategies[name] = s.External(cmd, timeouttime)
                else:
                    self.strategies[name].cmd = cmd
                    self.strategies[name].timeouttime = timeouttime

        else:
            self.error_message('指定された登録ファイルが見つかりませんでした')

    def error_message(self, message):
        """
        エラーメッセージを表示
        """
        root = tk.Tk()
        root.title('Error')
        root.minsize(300, 30)
        label = tk.Label(root, text=message)
        label.pack(fill='x', padx='5', pady='5')
        root.mainloop()

    def __demo(self):
        """
        デモ画面
        """
        while True:
            if self.window.start.event.is_set():
                self.window.start.event.clear()
                self.state = Reversi.PLAY
                break

            if not self._demo_animation():
                self.state = Reversi.INIT
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
                ('black', 'turnblack'),
                ('turnblack', 'white'),
                ('white', 'turnwhite'),
                ('turnwhite', 'black'),
            ],
            'white': [
                ('white', 'turnwhite'),
                ('turnwhite', 'black'),
                ('black', 'turnblack'),
                ('turnblack', 'white'),
            ],
        }

        for color, x, y in target:
            for remove_color, put_color in ptn[color]:
                # メニュー設定変更時
                if self._setting_changed():
                    return False

                # アニメーション処理
                time.sleep(TURN_DISC_WAIT)
                self.window.board.remove_disc(remove_color, x, y)
                self.window.board.put_disc(put_color, x, y)

        return True

    def __play(self):
        """
        ゲーム画面
        """
        self.window.set_state('disable')

        board = BitBoard(self.window.board.size)
        players = {}

        for color in ('black', 'white'):
            name = self.window.player[color]
            players[color] = Player(color, name, self.strategies[name])

        # ウィンドウの設定をゲームに反映
        s.common.Timer.time_limit = self.window.cputime

        game = Game(board, players['black'], players['white'], WindowDisplay(self.window), cancel=self.window.menu)
        game.play()

        time.sleep(1.5)  # 少し待って終了状態へ
        self.state = Reversi.END

    def __end(self):
        """
        終了画面
        """
        self.window.set_state('normal')

        while True:
            time.sleep(0.01)

            if self.window.start.event.is_set():
                self.window.start.event.clear()
                self.state = Reversi.REINIT
                break

            if self._setting_changed():
                self.state = Reversi.INIT
                break

    def __reinit(self):
        """
        再初期化(ゲーム終了後再スタート時)
        """
        self.window.init_screen()
        self.state = Reversi.PLAY

    def _setting_changed(self):
        """
        ウィンドウの設定が変更されたとき
        """
        if self.window.menu.event.is_set():
            self.window.size = self.window.menu.size
            self.window.player['black'] = self.window.menu.black_player
            self.window.player['white'] = self.window.menu.white_player
            self.window.assist = self.window.menu.assist
            self.window.language = self.window.menu.language
            self.window.menu.event.clear()

            return True

        return False


class Reversic:
    """
    リバーシゲーム
    """
    START, MENU, PLAY = 'START', 'MENU', 'PLAY'

    def __init__(self, strategies={}):
        self.board_size = 8
        self.player_names = {'black': 'User1', 'white': 'User2'}
        self.state = Reversic.START

        b, w = {}, {}
        b['User1'] = s.ConsoleUserInput()
        b.update(strategies)
        w['User2'] = s.ConsoleUserInput()
        w.update(strategies)
        self.strategies = {'black': b, 'white': w}

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

        if state == Reversic.START:
            self.game = self.__start
        elif state == Reversic.MENU:
            self.game = self.__menu
        else:
            self.game = self.__play

    def start(self):
        """
        アプリ開始
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
        self.state = Reversic.MENU

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
                self.state = Reversic.PLAY
                break
            elif user_in == 's':
                self.board_size = self._get_board_size()
                self.state = Reversic.START
                break
            elif user_in == 'b':
                self.player_names['black'] = self._get_player(self.strategies['black'])
                self.state = Reversic.START
                break
            elif user_in == 'w':
                self.player_names['white'] = self._get_player(self.strategies['white'])
                self.state = Reversic.START
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

            if MIN_BOARD_SIZE <= user_in <= MAX_BOARD_SIZE and not user_in % 2:
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
            selected_players[color] = Player(color, name, self.strategies[color][name])

        # ゲーム開始
        game = Game(board, selected_players['black'], selected_players['white'], ConsoleDisplay())
        game.play()

        # 少し待ってスタートに戻る
        time.sleep(2)
        self.state = Reversic.START
