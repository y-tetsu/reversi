#!/usr/bin/env python
"""
GUIウィンドウ
"""

import tkinter as tk
import board
from board import Board
import strategies


WINDOW_TITLE = 'othello'
WINDOW_WIDTH = 1360
WINDOW_HEIGHT = 680
BLACK_X_OFFSET = 200
WHITE_X_OFFSET = 1150
NAME_Y_OFFSET = 80
NUM_Y_OFFSET = 250
RESULT_Y_OFFSET = 400
TURN_Y_OFFSET = 500
MOVE_Y_OFFSET = 600
START_X_OFFSET = 680
START_Y_OFFSET = 620
COLOR_GREEN = 'green'
COLOR_BLACK = 'black'
COLOR_WHITE = 'white'
COLOR_ORANGE = 'orange'
COLOR_YELLOW = 'yellow'
COLOR_RED = 'red'
TEXT_FONT_SIZE = 32
SCORE_FONT_SIZE = 140
SQUARE_HEADER_FONT_SIZE = 20

SQUARE_Y_OFFSET = 40
SQUARE_BOTTOM_MARGIN = 120
OVAL_SIZE_RATIO = 0.8
TURNOVAL_SIZE_DIVISOR = 10
SQUARE_HEADER_OFFSET = 15

WINDOW_STATE_DEMO = 'DEMO'
WINDOW_STATE_GAME_START = 'GAME_START'

MENU_SIZE = 'Size'
MENU_BLACK = 'Black'
MENU_WHITE = 'White'

DEFAULT_BLACK_PLAYER = 'User1'
DEFAULT_WHITE_PLAYER = 'User2'
DEFAULT_BLACK_NUM = "2"
DEFAULT_WHITE_NUM = "2"

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


class Window(tk.Frame):
    """
    ウィンドウ
    """
    def __init__(self, size=8, master=None, event=None, queue=None):
        super().__init__(master)
        self.pack()

        self.size = size
        self.event = event  # GUIからのイベント発生通知
        self.queue = queue  # GUIからのデータ受け渡し

        self._create_game_screen()
        self._create_menu(master)

        self.state = WINDOW_STATE_DEMO
        self.black_player = DEFAULT_BLACK_PLAYER
        self.white_player = DEFAULT_WHITE_PLAYER

    def _create_game_screen(self):
        """
        ゲーム画面を配置
        """
        self.canvas = tk.Canvas(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=COLOR_GREEN)
        self.canvas.grid(row=0, column=0)

        self._create_text_on_canvas()
        self.init_board_on_canvas()

    def _create_menu(self, master):
        """
        メニューを配置
        """
        self.menubar = Menu(self, self.event, self.queue)  # メニューをセット
        master.configure(menu=self.menubar)

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
            BLACK_X_OFFSET,
            NAME_Y_OFFSET,
            text="●" + DEFAULT_BLACK_PLAYER,
            font=('', TEXT_FONT_SIZE),
            fill=COLOR_BLACK
        )

    def _create_white_name(self):
        """
        白のプレイヤー名の表示テキスト作成
        """
        self.white_name = self.canvas.create_text(
            WHITE_X_OFFSET,
            NAME_Y_OFFSET,
            text="●" + DEFAULT_WHITE_PLAYER,
            font=('', TEXT_FONT_SIZE),
            fill=COLOR_WHITE
        )

    def _create_black_stonenum(self):
        """
        黒の石の数の表示テキスト作成
        """
        self.black_stonenum = self.canvas.create_text(
            BLACK_X_OFFSET,
            NUM_Y_OFFSET,
            text=DEFAULT_BLACK_NUM,
            font=('', SCORE_FONT_SIZE),
            fill=COLOR_BLACK
        )

    def _create_white_stonenum(self):
        """
        白の石の数の表示テキスト作成
        """
        self.white_stonenum = self.canvas.create_text(
            WHITE_X_OFFSET,
            NUM_Y_OFFSET,
            text=DEFAULT_WHITE_NUM,
            font=('', SCORE_FONT_SIZE),
            fill=COLOR_WHITE
        )

    def _create_black_winlose(self):
        """
        黒の勝敗の表示テキスト作成
        """
        self.black_result = self.canvas.create_text(
            BLACK_X_OFFSET,
            RESULT_Y_OFFSET,
            text="",
            font=('', TEXT_FONT_SIZE),
            fill=COLOR_BLACK
        )

    def _create_white_winlose(self):
        """
        白の勝敗の表示テキスト作成
        """
        self.white_winlose = self.canvas.create_text(
            WHITE_X_OFFSET,
            RESULT_Y_OFFSET,
            text="",
            font=('', TEXT_FONT_SIZE),
            fill=COLOR_WHITE
        )

    def _create_black_turn(self):
        """
        黒の手番の表示テキスト作成
        """
        self.black_turn = self.canvas.create_text(
            BLACK_X_OFFSET,
            TURN_Y_OFFSET,
            text="",
            font=('', TEXT_FONT_SIZE),
            fill=COLOR_ORANGE
        )

    def _create_white_turn(self):
        """
        白の手番の表示テキスト作成
        """
        self.white_turn = self.canvas.create_text(
            WHITE_X_OFFSET,
            TURN_Y_OFFSET,
            text="",
            font=('', TEXT_FONT_SIZE),
            fill=COLOR_ORANGE
        )

    def _create_black_move(self):
        """
        黒の手の表示テキスト作成
        """
        self.black_move = self.canvas.create_text(
            BLACK_X_OFFSET,
            MOVE_Y_OFFSET,
            text="",
            font=('', TEXT_FONT_SIZE),
            fill=COLOR_BLACK
        )

    def _create_white_move(self):
        """
        白の手の表示テキスト作成
        """
        self.white_move = self.canvas.create_text(
            WHITE_X_OFFSET,
            MOVE_Y_OFFSET,
            text="",
            font=('', TEXT_FONT_SIZE),
            fill=COLOR_WHITE
        )

    def _create_start(self):
        """
        スタートボタンの作成
        """
        self.start = self.canvas.create_text(
            START_X_OFFSET,
            START_Y_OFFSET,
            text="クリックでスタート",
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
        self.canvas.itemconfigure(self.start, text='')

        self.menubar.entryconfigure(MENU_SIZE, state='disable')
        self.menubar.entryconfigure(MENU_BLACK, state='disable')
        self.menubar.entryconfigure(MENU_WHITE, state='disable')

        self.state = WINDOW_STATE_GAME_START

    def init_board_on_canvas(self):
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
        self.square_y_ini = SQUARE_Y_OFFSET
        self.square_w = (WINDOW_HEIGHT - self.square_y_ini - SQUARE_BOTTOM_MARGIN) // self.size
        self.square_x_ini = WINDOW_WIDTH // 2 - (self.square_w * self.size) // 2

        self.oval_w1 = int(self.square_w * OVAL_SIZE_RATIO)
        self.oval_w2 = int(self.square_w // TURNOVAL_SIZE_DIVISOR)

    def _draw_squares(self):
        """
        オセロのマスを描く
        """

        y1 = self.square_y_ini

        for y in range(self.size):
            x1 = self.square_x_ini
            y2 = y1 + self.square_w
            for x in range(self.size):
                label_x = chr(x + 97)
                label_y = str(y + 1)
                x2 = x1 + self.square_w

                if not x:
                    self.canvas.create_text(x1-SQUARE_HEADER_OFFSET, (y1+y2)//2, fill=COLOR_WHITE, text=label_y, tag='header_col', font=('', SQUARE_HEADER_FONT_SIZE))

                if not y:
                    self.canvas.create_text((x1+x2)//2, y1-SQUARE_HEADER_OFFSET, fill=COLOR_WHITE, text=label_x, tag='header_row', font=('', SQUARE_HEADER_FONT_SIZE))

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_GREEN, outline=COLOR_WHITE, tag='square_' + label_x + label_y)

                x1 = x2
            y1 = y2

    def _put_init_stones(self):
        """
        石を初期位置に置く
        """
        center = self.size // 2
        self.put_stone(Board.BLACK, center, center-1)
        self.put_stone(Board.BLACK, center-1, center)
        self.put_stone(Board.WHITE, center-1, center-1)
        self.put_stone(Board.WHITE, center, center)

    def put_stone(self, stone, index_x, index_y):
        """
        石を置く
        """
        if stone == Board.BLACK:
            self.put_black(index_x, index_y)
        elif stone == Board.WHITE:
            self.put_white(index_x, index_y)

    def put_black(self, index_x, index_y):
        """
        黒を置く
        """
        label = self.get_label("black", index_x, index_y)

        x, y = self.get_coordinate(index_x, index_y)

        x1 = x - self.oval_w1/2
        y1 = y - self.oval_w1/2
        x2 = x + self.oval_w1/2
        y2 = y + self.oval_w1/2

        black_id = self.canvas.create_oval(x1, y1, x2, y2, tag=label, fill=COLOR_BLACK, outline=COLOR_BLACK)

    def put_white(self, index_x, index_y):
        """
        白を置く
        """
        label = self.get_label("white", index_x, index_y)

        x, y = self.get_coordinate(index_x, index_y)

        x1 = x - self.oval_w1/2
        y1 = y - self.oval_w1/2
        x2 = x + self.oval_w1/2
        y2 = y + self.oval_w1/2

        white_id = self.canvas.create_oval(x1, y1, x2, y2, tag=label, fill=COLOR_WHITE, outline=COLOR_WHITE)

    def put_turnblack(self, index_x, index_y):
        """
        黒をひっくり返す途中
        """
        label1 = self.get_label("turnblack1", index_x, index_y)
        label2 = self.get_label("turnblack2", index_x, index_y)

        x, y = self.get_coordinate(index_x, index_y)

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
        label1 = self.get_label("turnwhite1", index_x, index_y)
        label2 = self.get_label("turnwhite2", index_x, index_y)

        x, y = self.get_coordinate(index_x, index_y)

        x1 = x - self.oval_w2
        y1 = y - self.oval_w1/2
        x2 = x
        y2 = y + self.oval_w1/2

        black_id = self.canvas.create_rectangle(x1, y1, x2, y2, tag=label1, fill=COLOR_BLACK, outline=COLOR_BLACK)

        x1 = x
        x2 = x + self.oval_w2
        white_id = self.canvas.create_rectangle(x1, y1, x2, y2, tag=label2, fill=COLOR_WHITE, outline=COLOR_WHITE)

    def clear_board_on_canvas(self):
        """
        ボードの石とマスをすべてクリア
        """
        self.remove_stones()
        self.remove_squares()

    def remove_stones(self):
        """
        すべての石を消す
        """
        for y in range(self.size):
            for x in range(self.size):
                self.remove_black(x, y)
                self.remove_white(x, y)
                self.remove_turnblack(x, y)
                self.remove_turnwhite(x, y)

    def remove_black(self, index_x, index_y):
        """
        黒を消す
        """
        label = self.get_label("black", index_x, index_y)
        self.canvas.delete(label)

    def remove_white(self, index_x, index_y):
        """
        白を消す
        """
        label = self.get_label("white", index_x, index_y)
        self.canvas.delete(label)

    def remove_turnblack(self, index_x, index_y):
        """
        黒ひっくり返し途中を消す
        """
        label1 = self.get_label("turnblack1", index_x, index_y)
        label2 = self.get_label("turnblack2", index_x, index_y)
        self.canvas.delete(label1)
        self.canvas.delete(label2)

    def remove_turnwhite(self, index_x, index_y):
        """
        白ひっくり返し途中を消す
        """
        label1 = self.get_label("turnwhite1", index_x, index_y)
        label2 = self.get_label("turnwhite2", index_x, index_y)
        self.canvas.delete(label1)
        self.canvas.delete(label2)

    def get_coordinate(self, index_x, index_y):
        """
        座標を計算する
        """
        x_ini = self.square_x_ini
        y_ini = self.square_y_ini
        w = self.square_w

        return x_ini + w * index_x + w // 2, y_ini + w * index_y + w // 2

    def remove_squares(self):
        """
        オセロのマスを消す
        """
        self.canvas.delete('header_col')
        self.canvas.delete('header_row')

        for y in range(self.size):
            for x in range(self.size):
                label = self.get_label('square', x, y)
                self.canvas.delete(label)

    def get_label(self, name, x, y):
        """
        表示ラベルを返す
        """
        return name + "_" + chr(x + 97) + str(y + 1)

    def reflect_board(self, board):
        """
        ボードの状態を反映する
        """
        board_info = board.get_board_info()
        print(board_info)

        for y in range(self.size):
            for x in range(self.size):
                stone = board_info[y][x]
                self.put_stone(board_info[y][x], x, y)


class Menu(tk.Menu):
    """
    メニュー
    """
    def __init__(self, master, event, queue):
        super().__init__(master)
        self.create_size_menu()
        self.create_black_menu()
        self.create_white_menu()
        self.event = event
        self.queue = queue

    def create_size_menu(self):
        """
        ボードのサイズ
        """
        menu_size = tk.Menu(self)
        for i in range(board.MIN_BOARD_SIZE, board.MAX_BOARD_SIZE + 1, 2):
            menu_size.add_command(label=str(i), command=self.change_board_size(i))
        self.add_cascade(menu=menu_size, label=MENU_SIZE)

    def create_black_menu(self):
        """
        黒プレイヤー
        """
        menu_black = tk.Menu(self)
        for player in BLACK_PLAYERS.keys():
            menu_black.add_command(label=player, command=self.change_black_player(player, self.master))
        self.add_cascade(menu=menu_black, label=MENU_BLACK)

    def create_white_menu(self):
        """
        白プレイヤー
        """
        menu_white = tk.Menu(self)
        for player in WHITE_PLAYERS.keys():
            menu_white.add_command(label=player, command=self.change_white_player(player, self.master))
        self.add_cascade(menu=menu_white, label=MENU_WHITE)

    def change_board_size(self, size):
        """
        ボードサイズの変更
        """
        def change_board_size_event():
            self.entryconfigure(MENU_SIZE, state='disable')

            if self.queue.empty():
                self.event.set()
                self.queue.put(size)

        return change_board_size_event

    def change_black_player(self, player, master):
        """
        黒プレーヤーを変更
        """
        def change_player():
            master.canvas.itemconfigure(master.black_name, text="●" + player)
            master.black_player = player

        return change_player

    def change_white_player(self, player, master):
        """
        白プレーヤーを変更
        """
        def change_player():
            master.canvas.itemconfigure(master.white_name, text="●" + player)
            master.white_player = player

        return change_player


if __name__ == '__main__':
    import time
    import threading
    import queue
    from player import Player

    event = threading.Event()
    q = queue.Queue()

    def demo(window):
        while True:
            if window.state == 'DEMO':
                # GUIメニューでサイズ変更時
                if event.is_set():
                    window.canvas.config(state='disable')

                    window.clear_board_on_canvas()  # 石とマスを消す
                    window.size = q.get()           # 変更後のサイズをセット
                    window.init_board_on_canvas()   # 石とマスの初期配置

                    event.clear()                   # イベントをクリア

                    window.canvas.config(state='normal')
                    window.menubar.entryconfigure(MENU_SIZE, state='normal')  # サイズメニューを有効にする

                center = window.size // 2

                for x, y in [(center, center-1), (center-1, center)]:
                    center = window.size // 2
                    time.sleep(0.1)
                    window.remove_black(x, y)
                    window.put_turnblack(x, y)

                    center = window.size // 2
                    time.sleep(0.1)
                    window.remove_turnblack(x, y)
                    window.put_white(x, y)

                    center = window.size // 2
                    time.sleep(0.1)
                    window.remove_white(x, y)
                    window.put_turnwhite(x, y)

                    center = window.size // 2
                    time.sleep(0.1)
                    window.remove_turnwhite(x, y)
                    window.put_black(x, y)

                for x, y in [(center-1, center-1), (center, center)]:
                    center = window.size // 2
                    time.sleep(0.1)
                    window.remove_white(x, y)
                    window.put_turnwhite(x, y)

                    center = window.size // 2
                    time.sleep(0.1)
                    window.remove_turnwhite(x, y)
                    window.put_black(x, y)

                    center = window.size // 2
                    time.sleep(0.1)
                    window.remove_black(x, y)
                    window.put_turnblack(x, y)

                    center = window.size // 2
                    time.sleep(0.1)
                    window.remove_turnblack(x, y)
                    window.put_white(x, y)

            if window.state == WINDOW_STATE_GAME_START:
                break

            window.menubar.entryconfigure(MENU_SIZE, state='normal')
            window.menubar.entryconfigure(MENU_BLACK, state='normal')
            window.menubar.entryconfigure(MENU_WHITE, state='normal')

        print("start", window.size, window.black_player, window.white_player)

        board = Board(window.size)
        black_player = Player(board.BLACK, window.black_player, BLACK_PLAYERS[window.black_player])
        white_player = Player(board.WHITE, window.white_player, WHITE_PLAYERS[window.white_player])

        while True:
            playable = 0

            moves = list(board.get_possibles(board.BLACK).keys())

            if moves:
                time.sleep(0.5)
                board.put(board.BLACK, *moves[0])
                window.reflect_board(board)
                playable += 1

            moves = list(board.get_possibles(board.WHITE).keys())

            if moves:
                time.sleep(0.5)
                board.put(board.WHITE, *moves[0])
                window.reflect_board(board)
                playable += 1

            if not playable:
                break

    app = tk.Tk()
    app.withdraw()  # 表示が整うまで隠す

    window = Window(master=app, event=event, queue=q)
    window.master.title(WINDOW_TITLE)                   # タイトル
    window.master.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)  # 最小サイズ

    game = threading.Thread(target=demo, args=([window]))
    game.daemon = True
    game.start()

    app.deiconify()  # 表示する
    app.mainloop()
