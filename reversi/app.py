"""Application
"""

import os
import time
import re
import tkinter as tk
import json
import threading

from reversi import BitBoard, MIN_BOARD_SIZE, MAX_BOARD_SIZE, Player, Window, WindowDisplay, ConsoleDisplay, Game, ErrorMessage, strategies


class Reversi:
    """
    リバーシゲーム
    """
    INIT, DEMO, PLAY, END, REINIT = 'INIT', 'DEMO', 'PLAY', 'END', 'REINIT'

    def __init__(self, players_info={}, turn_disc_wait=0.1, sleep_time_play=1.5, sleep_time_end=0.01):
        root = tk.Tk()
        root.withdraw()  # 表示が整うまで隠す

        self.state = Reversi.INIT

        b = ['User1'] + list(players_info.keys())
        w = ['User2'] + list(players_info.keys())
        self.window = Window(root=root, black_players=b, white_players=w)

        players_info['User1'] = strategies.WindowUserInput(self.window)
        players_info['User2'] = strategies.WindowUserInput(self.window)
        self.players_info = players_info

        self.err_msg = ErrorMessage()

        # wait or sleep time (sec)
        self.turn_disc_wait = turn_disc_wait
        self.sleep_time_play = sleep_time_play
        self.sleep_time_end = sleep_time_end

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
            if self.game():
                break

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
        game_thread = threading.Thread(target=self.gameloop)
        game_thread.daemon = True
        self._thread_start(game_thread)

    def _thread_start(self, thread):
        """
        スレッド開始
        """
        thread.start()

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
                name, cmd, timeouttime = None, None, None
                try:
                    # 設定の読み出し
                    json_dict = json.load(f)
                    name = json_dict['name']
                    cmd = json_dict['cmd']
                    timeouttime = json_dict['timeouttime']

                except Exception:
                    self.err_msg.show('フォーマットエラーのため登録ファイルが読み込めませんでした')

                else:
                    # メニューにAIの名前を追加
                    for color in ('black', 'white'):
                        if name not in self.window.menu.menu_items[color]:
                            self.window.menu.menu_items[color].append(name)
                            self.window.menu.menus[color].add_command(label=str(name), command=self.window.menu._command(color, name))

                    # 戦略を追加
                    self.players_info[name] = strategies.External(cmd, timeouttime)

        else:
            self.err_msg.show('指定された登録ファイルが見つかりませんでした')

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
                time.sleep(self.turn_disc_wait)
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
            players[color] = Player(color, name, self.players_info[name])

        # ウィンドウの設定をゲームに反映
        strategies.common.Timer.time_limit = self.window.cputime

        game = Game(board, players['black'], players['white'], WindowDisplay(self.window), cancel=self.window.menu)
        game.play()

        time.sleep(self.sleep_time_play)  # 少し待って終了状態へ
        self.state = Reversi.END

    def __end(self):
        """
        終了画面
        """
        self.window.set_state('normal')

        while True:
            time.sleep(self.sleep_time_end)

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

    def __init__(self, players_info={}, sleep_time_play=2):
        self.board_size = 8
        self.player_names = {'black': 'User1', 'white': 'User2'}
        self.state = Reversic.START

        b, w = {}, {}
        b['User1'] = strategies.ConsoleUserInput()
        b.update(players_info)
        w['User2'] = strategies.ConsoleUserInput()
        w.update(players_info)
        self.players_info = {'black': b, 'white': w}

        # sleep time(sec)
        self.sleep_time_play = sleep_time_play

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
            if self.game():
                break

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
                self.player_names['black'] = self._get_player(self.players_info['black'])
                self.state = Reversic.START
                break
            elif user_in == 'w':
                self.player_names['white'] = self._get_player(self.players_info['white'])
                self.state = Reversic.START
                break
            elif user_in == 'q':
                print('See you!')
                return True

    def _get_board_size(self):
        """
        ボードサイズの取得
        """
        print('press board size')

        while True:
            user_in = input('>> ')
            if re.match(r'^[1-9]+\d*$', user_in):
                size = int(user_in)
                if MIN_BOARD_SIZE <= size <= MAX_BOARD_SIZE and not size % 2:
                    return size

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
            user_in = input('>> ')
            if re.match(r'^[1-9]+\d*$', user_in):
                index = int(user_in)
                if 1 <= index <= len(player_list):
                    return player_list[index-1]

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
            selected_players[color] = Player(color, name, self.players_info[color][name])

        # ゲーム開始
        game = Game(board, selected_players['black'], selected_players['white'], ConsoleDisplay())
        game.play()

        # 少し待ってスタートに戻る
        time.sleep(self.sleep_time_play)
        self.state = Reversic.START
