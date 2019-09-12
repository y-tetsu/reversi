#!/usr/bin/env python
"""
GUIウィンドウ
"""

import time
import tkinter as tk

from stone import StoneFactory
import board
from board import Board
import strategies


WINDOW_TITLE = 'othello'
WINDOW_WIDTH = 1360
WINDOW_HEIGHT = 680

OFFSET_BLACK_X = 200
OFFSET_WHITE_X = 1150
OFFSET_NAME_Y = 80
OFFSET_NUM_Y = 250
OFFSET_RESULT_Y = 400
OFFSET_TURN_Y = 500
OFFSET_MOVE_Y = 600
OFFSET_START_X = 680
OFFSET_START_Y = 620
OFFSET_SQUARE_Y = 40
OFFSET_SQUARE_HEADER = 15

COLOR_GREEN = 'green'
COLOR_BLACK = 'black'
COLOR_WHITE = 'white'
COLOR_ORANGE = 'orange'
COLOR_YELLOW = 'yellow'
COLOR_RED = 'red'

TEXT_FONT_SIZE = 32
SCORE_FONT_SIZE = 140
SQUARE_HEADER_FONT_SIZE = 20

SQUARE_BOTTOM_MARGIN = 120
OVAL_SIZE_RATIO = 0.8
TURNOVAL_SIZE_DIVISOR = 10

MENU_NAME = {'size': 'Size', 'black': 'Black', 'white': 'White'}

START_TEXT = 'クリックでスタート'
STONE_MARK = '●'

TURN_STONE_WAIT = 0.1

DEFAULT_BLACK_PLAYER = 'User1'
DEFAULT_WHITE_PLAYER = 'User2'
DEFAULT_BLACK_NUM = "2"
DEFAULT_WHITE_NUM = "2"


class Window(tk.Frame):
    """
    ウィンドウ
    """
    def __init__(self, size=8, master=None, event=None, queue=None):
        super().__init__(master)
        self.pack()

        # 引数の取得
        self.size = size
        self.event = event  # ウィンドウからのイベント発生通知
        self.queue = queue  # ウィンドウからのデータ受け渡し

        # 石情報
        factory = StoneFactory()
        self.black = factory.create('black')
        self.white = factory.create('white')

        # 初期値設定
        self.master.title(WINDOW_TITLE)                   # タイトル
        self.master.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)  # 最小サイズ

        self.start_pressed = False
        self.wait_input = False
        self.black_player = DEFAULT_BLACK_PLAYER
        self.white_player = DEFAULT_WHITE_PLAYER

        # ウィンドウ初期化
        self._create_menu()
        self._create_game_screen()

    def _create_menu(self):
        """
        メニューを配置
        """
        self.menubar = Menu(self, self.event, self.queue)
        self.master.configure(menu=self.menubar)

    def _create_game_screen(self):
        """
        ゲーム画面を配置
        """
        self.canvas = tk.Canvas(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=COLOR_GREEN)
        self.canvas.grid(row=0, column=0)

    def init_game_screen(self):
        """
        ゲーム画面の初期化
        """
        # 全オブジェクト削除
        self._squares = []
        self.canvas.delete('all')

        # ボードを配置
        self._init_board_on_canvas()

        # テキストを配置
        self._create_text_on_canvas()

    def _create_text_on_canvas(self):
        """
        キャンバス上にテキストを配置
        """
        self._create_black_name()
        self._create_white_name()
        self._create_black_stonenum()
        self._create_white_stonenum()
        self._create_black_winlose()
        self._create_white_winlose()
        self._create_black_turn()
        self._create_white_turn()
        self._create_black_move()
        self._create_white_move()
        self._create_start()

    def _create_black_name(self):
        """
        黒のプレイヤー名の表示テキスト作成
        """
        self.black_name = self.canvas.create_text(
            OFFSET_BLACK_X,
            OFFSET_NAME_Y,
            text=STONE_MARK + self.black_player,
            font=('', TEXT_FONT_SIZE),
            fill=COLOR_BLACK
        )

    def _create_white_name(self):
        """
        白のプレイヤー名の表示テキスト作成
        """
        self.white_name = self.canvas.create_text(
            OFFSET_WHITE_X,
            OFFSET_NAME_Y,
            text=STONE_MARK + self.white_player,
            font=('', TEXT_FONT_SIZE),
            fill=COLOR_WHITE
        )

    def _create_black_stonenum(self):
        """
        黒の石の数の表示テキスト作成
        """
        self.black_stonenum = self.canvas.create_text(
            OFFSET_BLACK_X,
            OFFSET_NUM_Y,
            text=DEFAULT_BLACK_NUM,
            font=('', SCORE_FONT_SIZE),
            fill=COLOR_BLACK
        )

    def _create_white_stonenum(self):
        """
        白の石の数の表示テキスト作成
        """
        self.white_stonenum = self.canvas.create_text(
            OFFSET_WHITE_X,
            OFFSET_NUM_Y,
            text=DEFAULT_WHITE_NUM,
            font=('', SCORE_FONT_SIZE),
            fill=COLOR_WHITE
        )

    def _create_black_winlose(self):
        """
        黒の勝敗の表示テキスト作成
        """
        self.black_winlose = self.canvas.create_text(
            OFFSET_BLACK_X,
            OFFSET_RESULT_Y,
            text="",
            font=('', TEXT_FONT_SIZE),
            fill=COLOR_BLACK
        )

    def _create_white_winlose(self):
        """
        白の勝敗の表示テキスト作成
        """
        self.white_winlose = self.canvas.create_text(
            OFFSET_WHITE_X,
            OFFSET_RESULT_Y,
            text="",
            font=('', TEXT_FONT_SIZE),
            fill=COLOR_WHITE
        )

    def _create_black_turn(self):
        """
        黒の手番の表示テキスト作成
        """
        self.black_turn = self.canvas.create_text(
            OFFSET_BLACK_X,
            OFFSET_TURN_Y,
            text="",
            font=('', TEXT_FONT_SIZE),
            fill=COLOR_ORANGE
        )

    def _create_white_turn(self):
        """
        白の手番の表示テキスト作成
        """
        self.white_turn = self.canvas.create_text(
            OFFSET_WHITE_X,
            OFFSET_TURN_Y,
            text="",
            font=('', TEXT_FONT_SIZE),
            fill=COLOR_ORANGE
        )

    def _create_black_move(self):
        """
        黒の手の表示テキスト作成
        """
        self.black_move = self.canvas.create_text(
            OFFSET_BLACK_X,
            OFFSET_MOVE_Y,
            text="",
            font=('', TEXT_FONT_SIZE),
            fill=COLOR_BLACK
        )

    def _create_white_move(self):
        """
        白の手の表示テキスト作成
        """
        self.white_move = self.canvas.create_text(
            OFFSET_WHITE_X,
            OFFSET_MOVE_Y,
            text="",
            font=('', TEXT_FONT_SIZE),
            fill=COLOR_WHITE
        )

    def _create_start(self):
        """
        スタートボタンの作成
        """
        self.start = self.canvas.create_text(
            OFFSET_START_X,
            OFFSET_START_Y,
            text=START_TEXT,
            font=('', TEXT_FONT_SIZE),
            fill=COLOR_YELLOW
        )

        self.canvas.tag_bind(self.start, '<Enter>', self._enter_start)
        self.canvas.tag_bind(self.start, '<Leave>', self._leave_start)
        self.canvas.tag_bind(self.start, '<ButtonPress-1>', self._on_start)

    def _enter_start(self, event):
        """
        スタートボタンにカーソルが合った時
        """
        self.canvas.itemconfigure(self.start, fill=COLOR_RED)

    def _leave_start(self, event):
        """
        スタートボタンからカーソルが離れた時
        """
        self.canvas.itemconfigure(self.start, fill=COLOR_YELLOW)

    def _on_start(self, event):
        """
        スタートボタンを押した場合
        """
        self.disable_start()
        self.menubar.set_state('disable')

        self.start_pressed = True

    def _init_board_on_canvas(self):
        """
        盤面の表示の初期化
        """
        self._calc_size()        # 変更後の石やマスのサイズを計算
        self._draw_squares()     # マスの描画
        self._put_init_stones()  # 初期位置に石を置く

    def _calc_size(self):
        """
        サイズ計算
        """
        self.square_y_ini = OFFSET_SQUARE_Y
        self.square_w = (WINDOW_HEIGHT - self.square_y_ini - SQUARE_BOTTOM_MARGIN) // self.size
        self.square_x_ini = WINDOW_WIDTH // 2 - (self.square_w * self.size) // 2

        self.oval_w1 = int(self.square_w * OVAL_SIZE_RATIO)
        self.oval_w2 = int(self.square_w // TURNOVAL_SIZE_DIVISOR)

    def _draw_squares(self):
        """
        オセロのマスを描く
        """

        self._squares = [[None for _ in range(self.size)] for _ in range(self.size)]
        y1 = self.square_y_ini

        for y in range(self.size):
            x1 = self.square_x_ini
            y2 = y1 + self.square_w
            for x in range(self.size):
                label_x = chr(x + 97)
                label_y = str(y + 1)
                x2 = x1 + self.square_w

                if not x:
                    self.canvas.create_text(x1-OFFSET_SQUARE_HEADER, (y1+y2)//2, fill=COLOR_WHITE, text=label_y, tag='header_col', font=('', SQUARE_HEADER_FONT_SIZE))

                if not y:
                    self.canvas.create_text((x1+x2)//2, y1-OFFSET_SQUARE_HEADER, fill=COLOR_WHITE, text=label_x, tag='header_row', font=('', SQUARE_HEADER_FONT_SIZE))

                self._squares[y][x] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_GREEN, outline=COLOR_WHITE, tag='square_' + label_x + label_y)

                x1 = x2
            y1 = y2

    def _put_init_stones(self):
        """
        石を初期位置に置く
        """
        center = self.size // 2
        self.put_stone(self.black, center, center-1)
        self.put_stone(self.black, center-1, center)
        self.put_stone(self.white, center-1, center-1)
        self.put_stone(self.white, center, center)

    def put_stone(self, stone, index_x, index_y):
        """
        石を置く
        """
        if stone == self.black:
            self.put_black(index_x, index_y)
        elif stone == self.white:
            self.put_white(index_x, index_y)

    def put_black(self, index_x, index_y):
        """
        黒を置く
        """
        label = self._get_label("black", index_x, index_y)

        x, y = self._get_coordinate(index_x, index_y)

        x1 = x - self.oval_w1/2
        y1 = y - self.oval_w1/2
        x2 = x + self.oval_w1/2
        y2 = y + self.oval_w1/2

        black_id = self.canvas.create_oval(x1, y1, x2, y2, tag=label, fill=COLOR_BLACK, outline=COLOR_BLACK)

    def put_white(self, index_x, index_y):
        """
        白を置く
        """
        label = self._get_label("white", index_x, index_y)

        x, y = self._get_coordinate(index_x, index_y)

        x1 = x - self.oval_w1/2
        y1 = y - self.oval_w1/2
        x2 = x + self.oval_w1/2
        y2 = y + self.oval_w1/2

        white_id = self.canvas.create_oval(x1, y1, x2, y2, tag=label, fill=COLOR_WHITE, outline=COLOR_WHITE)

    def put_turnblack(self, index_x, index_y):
        """
        黒をひっくり返す途中
        """
        label1 = self._get_label("turnblack1", index_x, index_y)
        label2 = self._get_label("turnblack2", index_x, index_y)

        x, y = self._get_coordinate(index_x, index_y)

        x1 = x - self.oval_w2
        y1 = y - self.oval_w1/2
        x2 = x
        y2 = y + self.oval_w1/2

        white_id = self.canvas.create_rectangle(x1, y1, x2, y2, tag=label1, fill=COLOR_WHITE, outline=COLOR_WHITE)

        x1 = x
        x2 = x + self.oval_w2
        black_id = self.canvas.create_rectangle(x1, y1, x2, y2, tag=label2, fill=COLOR_BLACK, outline=COLOR_BLACK)

    def put_turnwhite(self, index_x, index_y):
        """
        白をひっくり返す途中
        """
        label1 = self._get_label("turnwhite1", index_x, index_y)
        label2 = self._get_label("turnwhite2", index_x, index_y)

        x, y = self._get_coordinate(index_x, index_y)

        x1 = x - self.oval_w2
        y1 = y - self.oval_w1/2
        x2 = x
        y2 = y + self.oval_w1/2

        black_id = self.canvas.create_rectangle(x1, y1, x2, y2, tag=label1, fill=COLOR_BLACK, outline=COLOR_BLACK)

        x1 = x
        x2 = x + self.oval_w2
        white_id = self.canvas.create_rectangle(x1, y1, x2, y2, tag=label2, fill=COLOR_WHITE, outline=COLOR_WHITE)

    def remove_black(self, index_x, index_y):
        """
        黒を消す
        """
        label = self._get_label("black", index_x, index_y)
        self.canvas.delete(label)

    def remove_white(self, index_x, index_y):
        """
        白を消す
        """
        label = self._get_label("white", index_x, index_y)
        self.canvas.delete(label)

    def remove_turnblack(self, index_x, index_y):
        """
        黒ひっくり返し途中を消す
        """
        label1 = self._get_label("turnblack1", index_x, index_y)
        label2 = self._get_label("turnblack2", index_x, index_y)
        self.canvas.delete(label1)
        self.canvas.delete(label2)

    def remove_turnwhite(self, index_x, index_y):
        """
        白ひっくり返し途中を消す
        """
        label1 = self._get_label("turnwhite1", index_x, index_y)
        label2 = self._get_label("turnwhite2", index_x, index_y)
        self.canvas.delete(label1)
        self.canvas.delete(label2)

    def _get_coordinate(self, index_x, index_y):
        """
        座標を計算する
        """
        x_ini = self.square_x_ini
        y_ini = self.square_y_ini
        w = self.square_w

        return x_ini + w * index_x + w // 2, y_ini + w * index_y + w // 2

    def _get_label(self, name, x, y):
        """
        表示ラベルを返す
        """
        return name + "_" + chr(x + 97) + str(y + 1)

    def turn_stone(self, stone, captures):
        """
        石をひっくり返す
        """
        if stone == self.black:
            self.turn_black_stone(captures)
        elif stone == self.white:
            self.turn_white_stone(captures)

    def turn_black_stone(self, captures):
        """
        白の石を黒の石にひっくり返す
        """
        # captures座標の白の石を消す
        for x, y in captures:
            self.remove_white(x, y)

        # captures座標に白をひっくり返す途中の石を置く
        for x, y in captures:
            self.put_turnwhite(x, y)
        time.sleep(TURN_STONE_WAIT)

        # captures座標の白をひっくり返す途中の石を消す
        for x, y in captures:
            self.remove_turnwhite(x, y)

        # capturesの石を黒にする
        for x, y in captures:
            self.put_black(x, y)
        time.sleep(TURN_STONE_WAIT)

    def turn_white_stone(self, captures):
        """
        黒の石を白の石にひっくり返す
        """
        # captures座標の黒の石を消す
        for x, y in captures:
            self.remove_black(x, y)

        # captures座標に黒をひっくり返す途中の石を置く
        for x, y in captures:
            self.put_turnblack(x, y)
        time.sleep(TURN_STONE_WAIT)

        # captures座標の黒をひっくり返す途中の石を消す
        for x, y in captures:
            self.remove_turnblack(x, y)

        # capturesの石を白にする
        for x, y in captures:
            self.put_white(x, y)
        time.sleep(TURN_STONE_WAIT)

    def disable_window(self):
        """
        ウィンドウを無効化
        """
        self.disable_start()
        self.disable_canvas()
        self.menubar.set_state('disable')

    def enable_window(self):
        """
        ウィンドウを有効化
        """
        self.menubar.set_state('normal')
        self.enable_canvas()
        self.enable_start()

    def disable_start(self):
        """
        スタートを無効化
        """
        self.canvas.itemconfigure(self.start, text='', state='disable')

    def enable_start(self):
        """
        スタートを有効化
        """
        self.canvas.itemconfigure(self.start, text=START_TEXT, state='normal')

    def disable_canvas(self):
        """
        キャンバスを無効化
        """
        self.canvas.config(state='disable')

    def enable_canvas(self):
        """
        キャンバスを有効化
        """
        self.canvas.config(state='normal')

    def enable_moves(self, moves):
        """
        打てる場所をハイライトする
        """
        for x, y in moves:
            square = self._squares[y][x]
            self.canvas.itemconfigure(square, fill=COLOR_YELLOW)

    def disable_moves(self, moves):
        """
        打てる場所のハイライトを元に戻す
        """
        for x, y in moves:
            square = self._squares[y][x]
            self.canvas.itemconfigure(square, fill=COLOR_GREEN)

    def enable_move(self, x, y):
        """
        打った場所をハイライトする
        """
        square = self._squares[y][x]
        self.canvas.itemconfigure(square, fill=COLOR_RED)

    def disable_move(self, x, y):
        """
        打った場所のハイライトを元に戻す
        """
        square = self._squares[y][x]
        self.canvas.itemconfigure(square, fill=COLOR_GREEN)

    def selectable_moves(self, moves):
        """
        打てる場所を選択できるようにする
        """
        for x, y in moves:
            square = self._squares[y][x]
            self.canvas.tag_bind(square, '<Enter>', self._enter_selectable_moves(square))
            self.canvas.tag_bind(square, '<Leave>', self._leave_selectable_moves(square))
            self.canvas.tag_bind(square, '<ButtonPress-1>', self._press_selectable_moves(x, y))

    def unselectable_moves(self, moves):
        """
        打てる場所を選択できないようにする
        """
        for x, y in moves:
            square = self._squares[y][x]
            self.canvas.tag_bind(square, '<Enter>', lambda *args: None)
            self.canvas.tag_bind(square, '<Leave>', lambda *args: None)
            self.canvas.tag_bind(square, '<ButtonPress-1>', lambda *args: None)

    def _enter_selectable_moves(self, square):
        """
        打てる場所にカーソルが合ったとき
        """
        def _enter(event):
            self.canvas.itemconfigure(square, fill=COLOR_RED)

        return _enter

    def _leave_selectable_moves(self, square):
        """
        打てる場所からカーソルが離れた
        """
        def _leave(event):
            self.canvas.itemconfigure(square, fill=COLOR_YELLOW)

        return _leave

    def _press_selectable_moves(self, x, y):
        """
        打てる場所をクリックしたとき
        """
        def _press(event):
            if self.wait_input:
                self.wait_input = False
                self.queue.put((x, y))

        return _press


class Menu(tk.Menu):
    """
    メニュー
    """
    def __init__(self, window=None, event=None, queue=None):
        super().__init__(window.master)

        # 引数取得
        self.window = window
        self.event = event
        self.queue = queue

        # プレイヤーの生成
        self._create_players()

        # メニューの生成
        menus = {
            'size': range(board.MIN_BOARD_SIZE, board.MAX_BOARD_SIZE + 1, 2),
            'black': self.black_players.keys(),
            'white': self.white_players.keys(),
        }

        for name, items in menus.items():
            self._create_menu(name, items)

    def _create_players(self):
        self.black_players = {
            'User1': strategies.WindowUserInput(self.window),
            'Random': strategies.Random(),
            'Greedy': strategies.Greedy(),
            'Unselfish': strategies.Unselfish(),
        }

        self.white_players = {
            'User2': strategies.WindowUserInput(self.window),
            'Random': strategies.Random(),
            'Greedy': strategies.Greedy(),
            'Unselfish': strategies.Unselfish(),
        }

    def _create_menu(self, name, items):
        """
        メニューの追加
        """
        menu = tk.Menu(self)

        for item in items:
            menu.add_command(label=str(item), command=self._command(name, item))

        self.add_cascade(menu=menu, label=MENU_NAME[name])

    def _command(self, name, item):
        """
        メニュー設定変更時
        """
        def change_menu_selection():
            if self.queue.empty():
                size = item if name == 'size' else self.window.size
                black = item if name == 'black' else self.window.black_player
                white = item if name == 'white' else self.window.white_player

                # ウィンドウ無効化
                self.window.disable_window()

                # 設定変更を通知
                self.event.set()
                self.queue.put((size, black, white))

        return change_menu_selection

    def set_state(self, state):
        """
        メニューのステータス設定(有効化/無効化)
        """
        for name in MENU_NAME.values():
            self.entryconfigure(name, state=state)


if __name__ == '__main__':
    import time
    import threading
    import queue
    from player import Player

    event = threading.Event()
    q = queue.Queue()

    state = 'INIT'

    def resize_board(window):
        global state

        if event.is_set():
            window.size, window.black_player, window.white_player = q.get()  # 変更後のサイズをセット
            state = 'INIT'                                                   # ウィンドウ初期化
            event.clear()                                                    # イベントをクリア

            return True

        return False

    def test_play(window):
        global state

        demo = False

        while True:
            resize_board(window)

            if state == 'INIT':
                demo = False
                window.init_game_screen()
                window.enable_window()
                state = 'DEMO'

            if state == 'DEMO':
                demo = True
                resize_flag = False
                center = window.size // 2

                for x, y in [(center, center-1), (center-1, center)]:
                    if resize_board(window):
                        resize_flag = True
                        break

                    center = window.size // 2
                    time.sleep(TURN_STONE_WAIT)
                    window.remove_black(x, y)
                    window.put_turnblack(x, y)

                    if resize_board(window):
                        resize_flag = True
                        break

                    center = window.size // 2
                    time.sleep(TURN_STONE_WAIT)
                    window.remove_turnblack(x, y)
                    window.put_white(x, y)

                    if resize_board(window):
                        resize_flag = True
                        break

                    center = window.size // 2
                    time.sleep(TURN_STONE_WAIT)
                    window.remove_white(x, y)
                    window.put_turnwhite(x, y)

                    if resize_board(window):
                        resize_flag = True
                        break

                    center = window.size // 2
                    time.sleep(TURN_STONE_WAIT)
                    window.remove_turnwhite(x, y)
                    window.put_black(x, y)

                if not resize_flag:
                    center = window.size // 2

                    for x, y in [(center-1, center-1), (center, center)]:
                        if resize_board(window):
                            break

                        center = window.size // 2
                        time.sleep(TURN_STONE_WAIT)
                        window.remove_white(x, y)
                        window.put_turnwhite(x, y)

                        if resize_board(window):
                            break

                        center = window.size // 2
                        time.sleep(TURN_STONE_WAIT)
                        window.remove_turnwhite(x, y)
                        window.put_black(x, y)

                        if resize_board(window):
                            break

                        center = window.size // 2
                        time.sleep(TURN_STONE_WAIT)
                        window.remove_black(x, y)
                        window.put_turnblack(x, y)

                        if resize_board(window):
                            break

                        center = window.size // 2
                        time.sleep(TURN_STONE_WAIT)
                        window.remove_turnblack(x, y)
                        window.put_white(x, y)

                if window.start_pressed:
                    window.start_pressed = False
                    state = 'START'

            if state == 'START':
                if not demo:
                    window.init_game_screen()
                    window.disable_start()
                    window.menubar.set_state('disable')

                demo = False
                print("start", window.size, window.black_player, window.white_player)

                board = Board(window.size)
                black_player = Player(board.black, window.black_player, window.menubar.black_players[window.black_player])
                white_player = Player(board.white, window.white_player, window.menubar.white_players[window.white_player])

                while True:
                    playable = 0

                    moves = list(board.get_possibles(board.black).keys())

                    if moves:
                        window.enable_moves(moves)
                        window.selectable_moves(moves)

                        time.sleep(0.2)
                        black_player.put_stone(board)

                        window.disable_moves(moves)
                        window.enable_move(*black_player.move)

                        window.put_stone(board.black, *black_player.move)

                        time.sleep(1.2)
                        window.turn_stone(board.black, black_player.captures)

                        window.unselectable_moves(moves)
                        window.disable_move(*black_player.move)

                        playable += 1

                    moves = list(board.get_possibles(board.white).keys())

                    if moves:
                        window.enable_moves(moves)

                        time.sleep(0.2)
                        white_player.put_stone(board)

                        window.disable_moves(moves)
                        window.enable_move(*white_player.move)

                        window.put_stone(board.white, *white_player.move)

                        time.sleep(1.2)
                        window.turn_stone(board.white, white_player.captures)
                        window.disable_move(*white_player.move)

                        playable += 1

                    if not playable:
                        state = 'END'
                        window.enable_window()
                        break

            if state == 'END':
                demo = False

                if window.start_pressed:
                    window.start_pressed = False
                    state = 'START'

    app = tk.Tk()
    app.withdraw()  # 表示が整うまで隠す

    window = Window(master=app, event=event, queue=q)

    game = threading.Thread(target=test_play, args=([window]))
    game.daemon = True
    game.start()

    app.deiconify()  # 表示する
    app.mainloop()
