"""Application
"""

import os
import time
import datetime
import re
import tkinter as tk
import json
import threading
from platform import system
from ctypes import windll

from reversi import BitBoard, MIN_BOARD_SIZE, MAX_BOARD_SIZE, Player, Window, WindowDisplay, ConsoleDisplay, Game, ErrorMessage, strategies, X, Recorder


class Reversi:
    """
    リバーシゲーム
    """
    INIT, DEMO, PLAY, END, REINIT = 'INIT', 'DEMO', 'PLAY', 'END', 'REINIT'

    def __init__(self, players_info={}, turn_disc_wait=0.1, sleep_time_play=1.5, sleep_time_end=0.01, sleep_time_turn=0.3, sleep_time_move=0.3):
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
        self.sleep_time_turn = sleep_time_turn
        self.sleep_time_move = sleep_time_move

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
            with open(extra_file, 'r', encoding='utf-8') as f:
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

        Game(
            players['black'],
            players['white'],
            board,
            WindowDisplay(self.window, sleep_time_turn=self.sleep_time_turn, sleep_time_move=self.sleep_time_move),
            cancel=self.window.menu,
        ).play()

        if self.window.record == 'ON':
            t_delta = datetime.timedelta(hours=9)
            JST = datetime.timezone(t_delta, 'JST')
            now = datetime.datetime.now(JST)
            black_name = players['black'].name
            white_name = players['white'].name
            record_name = now.strftime('%Y%m%d%H%M%S') + '_' + black_name + '_vs_' + white_name + '.txt'
            with open(record_name, 'w', encoding='utf-8') as f:
                f.write('\n')
                f.write('-------------------------------------------\n')
                f.write(now.strftime('%Y/%m/%d %H:%M:%S') + '\n')
                f.write('-------------------------------------------\n')
                f.write('\n')
                f.write(str(board) + '\n')
                f.write("(black:" + black_name + ") " + str(board._black_score) + " - " + str(board._white_score) + " (white:" + white_name + ")\n")
                f.write(str(Recorder(board)) + '\n')

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
            self.window.record = self.window.menu.record
            self.window.menu.event.clear()

            return True

        return False


class Reversic:
    """
    リバーシゲーム
    """
    START, MENU, PLAY = 'START', 'MENU', 'PLAY'

    def __init__(self, players_info={}, sleep_time_play=2, sleep_time_turn=1, sleep_time_move=1):
        self.board_type = 'Square-8'
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
        self.sleep_time_turn = sleep_time_turn
        self.sleep_time_move = sleep_time_move

        if 'win' in system().lower():
            kernel = windll.kernel32
            kernel.SetConsoleMode(kernel.GetStdHandle(-11), 7)

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
        try:
            while True:
                if self.game():
                    break
        except KeyboardInterrupt:
            return

    def __start(self):
        """
        設定を表示
        """
        self._clear_screen()

        print('\n=============================')
        print('BoardType   =', self.board_type)
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
        print(' t      : change board type')
        print(' b      : change black player')
        print(' w      : change white player')
        print(' q      : quit')
        print('-----------------------------')

        while True:
            user_in = input('>> ')

            if not user_in:
                self.state = Reversic.PLAY
                break
            elif user_in == 't':
                self.board_type = self._get_board_type()
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

    def _clear_screen(self):
        print("\033[;H\033[2J")

    def _get_board_type(self):
        """
        ボードタイプの取得
        """
        self._clear_screen()

        board_list = list(X.keys())

        print('select board type')
        print('-----------------------------')
        for num, value in enumerate(board_list, 1):
            print(f' {num:2d} : {value}')
        print('-----------------------------')

        while True:
            user_in = input('>> ')
            if re.match(r'^[1-9]+\d*$', user_in):
                index = int(user_in)
                if 1 <= index <= len(board_list):
                    return board_list[index-1]

    def _get_player(self, players):
        """
        プレイヤーの取得
        """
        self._clear_screen()

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
        self._clear_screen()

        # ボード準備
        hole = X[self.board_type][0]
        ini_black = X[self.board_type][1]
        ini_white = X[self.board_type][2]
        board = BitBoard(hole=hole, ini_black=ini_black, ini_white=ini_white)

        # プレイヤー準備
        selected_players = {}

        for color in ('black', 'white'):
            name = self.player_names[color]
            selected_players[color] = Player(color, name, self.players_info[color][name])

        # ゲーム開始
        Game(
            selected_players['black'],
            selected_players['white'],
            board,
            ConsoleDisplay(sleep_time_turn=self.sleep_time_turn, sleep_time_move=self.sleep_time_move),
        ).play()

        # Enterでスタートに戻る
        self._wait_enter()
        self.state = Reversic.START

    def _wait_enter(self):
        input('\nPress "Enter" to return.')
