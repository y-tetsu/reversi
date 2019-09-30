#!/usr/bin/env python
"""
GUIウィンドウ
"""

import time
import tkinter as tk
import threading

import board
from board import Board
import strategies


WINDOW_TITLE = 'othello'  # ウィンドウのタイトル
WINDOW_WIDTH = 1360       # ウィンドウ幅
WINDOW_HEIGHT = 680       # ウィンドウ高さ

COLOR_GREEN = 'green'    # 緑
COLOR_BLACK = 'black'    # 黒
COLOR_WHITE = 'white'    # 白
COLOR_ORANGE = 'orange'  # オレンジ
COLOR_YELLOW = 'yellow'  # 黄
COLOR_RED = 'red'        # 赤

INFO_OFFSET_X = {  # 表示テキストのXオフセット
    'black':  200,
    'white': 1150,
}
INFO_OFFSET_Y = {  # 表示テキストのYオフセット
    'name':     80,
    'score':   250,
    'winlose': 400,
    'turn':    500,
    'move':    600,
}
INFO_COLOR = {  # 表示テキストの色
    'name':    {'black': COLOR_BLACK,  'white': COLOR_WHITE},
    'score':   {'black': COLOR_BLACK,  'white': COLOR_WHITE},
    'winlose': {'black': COLOR_BLACK,  'white': COLOR_WHITE},
    'turn':    {'black': COLOR_ORANGE, 'white': COLOR_ORANGE},
    'move':    {'black': COLOR_BLACK,  'white': COLOR_WHITE},
}
INFO_FONT_SIZE = {  # 表示テキストのフォントサイズ
    'name':     32,
    'score':   140,
    'winlose':  32,
    'turn':     32,
    'move':     32,
}

START_OFFSET_X = 680              # スタートのXオフセット
START_OFFSET_Y = 620              # スタートのYオフセット
START_FONT_SIZE = 32              # スタートのフォントサイズ
START_TEXT = 'クリックでスタート' # スタートのテキスト

ASSIST_OFFSET_X = 50   # アシストのXオフセット
ASSIST_OFFSET_Y = 20   # アシストのYオフセット
ASSIST_FONT_SIZE = 12  # アシストのフォントサイズ

SQUAREHEADER_OFFSET_XY = 15  # マス目の列見出しのXYオフセット
SQUAREHEADER_FONT_SIZE = 20  # マス目の列見出しのフォントサイズ

SQUARE_OFFSET_Y = 40        # マス目のYオフセット
SQUARE_BOTTOM_MARGIN = 120  # マス目の底部のマージン
OVAL_SIZE_RATIO = 0.8       # マス目に対する石の円のサイズの割合
TURNOVAL_SIZE_DIVISOR = 10  # 石をひっくり返す途中のサイズ(マス目の何分の1か)

TURN_BLACK_PATTERN = [('white', 'turnwhite'), ('turnwhite', 'black')]  # 黒の石をひっくり返すパターン
TURN_WHITE_PATTERN = [('black', 'turnblack'), ('turnblack', 'white')]  # 白の石をひっくり返すパターン
TURN_STONE_WAIT = 0.1                                                  # 石をひっくり返す待ち時間(s)

ASSIST_MENU = ['ON', 'OFF']  # 打てる場所のハイライト表示の有無

STONE_MARK = '●'      # 石のマーク

DEFAULT_BOARD_SIZE = 8   # ボードサイズの初期値
DEFAULT_BLACK_NUM = '2'  # 黒の石の数初期値
DEFAULT_WHITE_NUM = '2'  # 白の石の数初期値
DEFAULT_INFO_TEXT = {    # 表示テキストのテキスト初期値
    'name':    {'black': lambda s: STONE_MARK + s.player['black'], 'white': lambda s: STONE_MARK + s.player['white']},
    'score':   {'black': lambda s: '2',                            'white': lambda s: '2'                           },
    'winlose': {'black': lambda s: '',                             'white': lambda s: ''                            },
    'turn':    {'black': lambda s: '',                             'white': lambda s: ''                            },
    'move':    {'black': lambda s: '',                             'white': lambda s: ''                            },
}


class Window(tk.Frame):
    """
    ウィンドウ
    """
    def __init__(self, root=None, black_players=None, white_players=None):
        super().__init__(root)
        self.pack()

        # 初期設定
        self.size = DEFAULT_BOARD_SIZE
        self.player = {'black': black_players[0], 'white': white_players[0]}
        self.assist = ASSIST_MENU[0]

        # ウィンドウ設定
        root.title(WINDOW_TITLE)                   # タイトル
        root.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)  # 最小サイズ

        # メニューを配置
        self.menu = Menu(root, black_players, white_players)
        root.configure(menu=self.menu)

        # キャンバスを配置
        self.canvas = tk.Canvas(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=COLOR_GREEN)
        self.canvas.grid(row=0, column=0)

    def init_screen(self):
        """
        ゲーム画面の初期化
        """
        self.canvas.delete('all')                                      # 全オブジェクト削除
        self.board = ScreenBoard(self.canvas, self.size, self.assist)  # ボード配置
        self.info = ScreenInfo(self.canvas, self.player)               # 情報表示テキスト配置
        self.start = ScreenStart(self.canvas)                          # スタートテキスト配置

    def set_state(self, state):
        """
        ウィンドウを有効化/無効化
        """
        self.start.set_state(state)
        self.menu.set_state(state)


class Menu(tk.Menu):
    """
    メニュー
    """
    def __init__(self, root, black_players, white_players):
        super().__init__(root)

        self.size = DEFAULT_BOARD_SIZE
        self.black_player = black_players[0]
        self.white_player = white_players[0]
        self.assist = ASSIST_MENU[0]
        self.menu_items = {}

        # イベントの生成
        self.event = threading.Event()

        # メニューアイテムの生成
        self.menu_items['size'] = range(board.MIN_BOARD_SIZE, board.MAX_BOARD_SIZE + 1, 2)
        self.menu_items['black'] = black_players
        self.menu_items['white'] = white_players
        self.menu_items['assist'] = ASSIST_MENU
        self._create_menu_items()

    def _create_menu_items(self):
        """
        メニューの追加
        """
        for name, items in self.menu_items.items():
            menu = tk.Menu(self, tearoff=False)

            for item in items:
                menu.add_command(label=str(item), command=self._command(name, item))

            self.add_cascade(menu=menu, label=name.title())

    def _command(self, name, item):
        """
        メニュー設定変更時
        """
        def change_menu_selection():
            if not self.event.is_set():
                self.size = item if name == 'size' else self.size
                self.black_player = item if name == 'black' else self.black_player
                self.white_player= item if name == 'white' else self.white_player
                self.assist= item if name == 'assist' else self.assist
                self.event.set()  # ウィンドウへメニューの設定変更を通知

        return change_menu_selection

    def set_state(self, state):
        """
        メニューのステータス設定(有効化/無効化)
        """
        for name in self.menu_items.keys():
            self.entryconfigure(name.title(), state=state)


class ScreenBoard:
    """
    ボードの表示
    """
    def __init__(self, canvas, size, assist):
        self.size = size
        self.assist = assist
        self.canvas = canvas
        self._squares = []
        self._xlines = []
        self._ylines = []
        self.move = None

        # イベント生成
        self.event = threading.Event()

        # アシスト表示
        assist_text = 'Assist Off' if self.assist == 'OFF' else ''
        self.text = canvas.create_text(
            ASSIST_OFFSET_X,
            ASSIST_OFFSET_Y,
            text=assist_text,
            font=('', ASSIST_FONT_SIZE),
            fill=COLOR_WHITE
        )

        # ボードの描画
        self._draw_squares()

    def _draw_squares(self):
        """
        マス目を描画
        """
        size = self.size
        self._squares = [[None for _ in range(size)] for _ in range(size)]

        # マス目や石のサイズを計算
        self.square_y_ini = SQUARE_OFFSET_Y
        self.square_w = (WINDOW_HEIGHT - self.square_y_ini - SQUARE_BOTTOM_MARGIN) // size
        w = self.square_w
        self.square_x_ini = WINDOW_WIDTH // 2 - (w * size) // 2
        self.oval_w1 = int(w * OVAL_SIZE_RATIO)
        self.oval_w2 = int(w // TURNOVAL_SIZE_DIVISOR)

        # マス目や見出しの位置を初期化
        min_x, min_y = self.square_x_ini, self.square_y_ini
        max_x, max_y = min_x + w * size, min_y + w * size
        row_x, col_y = min_x - SQUAREHEADER_OFFSET_XY, min_y - SQUAREHEADER_OFFSET_XY
        label = None
        text_x, text_y = None, None
        square_x1, square_y1, square_x2, square_y2 = None, None, None, None
        line_append, xappend, yappend = None, self._xlines.append, self._ylines.append

        # マス目の描画
        for num in range(size + 1):
            for rc in ('row', 'col'):
                if rc == 'row':
                    label = str(num + 1)
                    text_x, text_y = row_x, (min_y + w * num) + w // 2
                    square_x1, square_y1 = min_x + w * num, min_y
                    square_x2, square_y2 = square_x1, max_y
                    line_append = yappend
                else:
                    label = chr(num + 97)
                    text_x, text_y = (min_x + w * num) + w // 2, col_y
                    square_x1, square_y1 = min_x, min_y + w * num
                    square_x2, square_y2 = max_x, square_y1
                    line_append = xappend

                # 番地
                if num < size:
                    self.canvas.create_text(text_x, text_y, fill=COLOR_WHITE, text=label, font=('', SQUAREHEADER_FONT_SIZE))

                # マス目の線
                line = self.canvas.create_line(square_x1, square_y1, square_x2, square_y2, fill=COLOR_WHITE)
                line_append(line)

        # 初期位置に石を置く
        center = size // 2
        self.put_stone('black', center, center-1)
        self.put_stone('black', center-1, center)
        self.put_stone('white', center-1, center-1)
        self.put_stone('white', center, center)

    def put_stone(self, color, index_x, index_y):
        """
        石を置く
        """
        x, y = self._get_coordinate(index_x, index_y)

        # 黒か白の石をおく
        if color == 'black' or color == 'white':
            w = self.oval_w1
            x1, y1, x2, y2 = x - w/2, y - w/2, x + w/2, y + w/2
            label = self._get_label(color, index_x, index_y)

            self.canvas.create_oval(x1, y1, x2, y2, tag=label, fill=color, outline=color)

        # ひっくり返す途中
        else:
            w1, w2 = self.oval_w1, self.oval_w2
            label1 = self._get_label(color + '1', index_x, index_y)
            label2 = self._get_label(color + '2', index_x, index_y)
            color1 = 'white' if color == 'turnblack' else 'black'
            color2 = 'black' if color == 'turnblack' else 'white'

            x1, y1, x2, y2 = x - w2, y - w1/2, x, y + w1/2
            self.canvas.create_rectangle(x1, y1, x2, y2, tag=label1, fill=color1, outline=color1)

            x3, x4 = x, x + w2
            self.canvas.create_rectangle(x3, y1, x4, y2, tag=label2, fill=color2, outline=color2)

    def remove_stone(self, color, index_x, index_y):
        """
        石を消す
        """
        ptns = []
        if color == 'black' or color == 'white':
            ptns = [color]
        else:
            ptns = [color + str(i) for i in range(1, 3)]

        for ptn in ptns:
            label = self._get_label(ptn, index_x, index_y)
            self.canvas.delete(label)

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
        return name + '_' + chr(x + 97) + str(y + 1)

    def turn_stone(self, color, captures):
        """
        石をひっくり返す
        """
        ptn = TURN_BLACK_PATTERN if color == 'black' else TURN_WHITE_PATTERN

        for remove_color, put_color in ptn:
            for x, y in captures:
                self.remove_stone(remove_color, x, y)
            for x, y in captures:
                self.put_stone(put_color, x, y)
            time.sleep(TURN_STONE_WAIT)

    def enable_moves(self, moves):
        """
        打てる場所をハイライトする
        """
        for x, y in moves:
            x1 = self.square_x_ini + self.square_w * x
            x2 = x1 + self.square_w
            y1 = self.square_y_ini + self.square_w * y
            y2 = y1 + self.square_w
            if self.assist == 'ON':
                self._squares[y][x] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_YELLOW, outline=COLOR_WHITE, tag='moves')
            else:
                self._squares[y][x] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_GREEN, outline=COLOR_WHITE, tag='moves')

    def disable_moves(self, moves):
        """
        打てる場所のハイライトを元に戻す
        """
        self.canvas.delete('moves')

    def enable_move(self, x, y):
        """
        打った場所をハイライトする
        """
        x1 = self.square_x_ini + self.square_w * x
        x2 = x1 + self.square_w
        y1 = self.square_y_ini + self.square_w * y
        y2 = y1 + self.square_w
        self._squares[y][x] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_RED, outline=COLOR_WHITE, tag='move')

    def disable_move(self, x, y):
        """
        打った場所のハイライトを元に戻す
        """
        self.canvas.delete('move')

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
            if self.assist == 'ON':
                self.canvas.itemconfigure(square, fill=COLOR_RED)

        return _enter

    def _leave_selectable_moves(self, square):
        """
        打てる場所からカーソルが離れた
        """
        def _leave(event):
            if self.assist == 'ON':
                self.canvas.itemconfigure(square, fill=COLOR_YELLOW)

        return _leave

    def _press_selectable_moves(self, x, y):
        """
        打てる場所をクリックしたとき
        """
        def _press(event):
            if not self.event.is_set():
                self.move = (x, y)
                self.event.set()  # ウィンドウへ手の選択を通知

        return _press


class ScreenInfo:
    """
    情報表示テキスト
    """
    def __init__(self, canvas, player):
        self.canvas = canvas
        self.player = player
        self.text = {}

        # テキスト作成
        for name in INFO_OFFSET_Y.keys():
            for color in INFO_OFFSET_X.keys():
                self._create_text(color, name)  # 表示テキスト

    def _create_text(self, color, name):
        """
        表示テキスト作成
        """
        self.text[color + '_' + name] = self.canvas.create_text(
            INFO_OFFSET_X[color],
            INFO_OFFSET_Y[name],
            text=DEFAULT_INFO_TEXT[name][color](self),
            font=('', INFO_FONT_SIZE[name]),
            fill=INFO_COLOR[name][color]
        )

    def set_text(self, color, name, text):
        """
        表示テキストの文字列を設定
        """
        text_id = self.text[color + '_' + name]
        self.canvas.itemconfigure(text_id, text=text)


class ScreenStart:
    """
    スタートテキスト
    """
    def __init__(self, canvas):
        self.canvas = canvas

        # テキスト作成
        self.text = canvas.create_text(
            START_OFFSET_X,
            START_OFFSET_Y,
            text=START_TEXT,
            font=('', START_FONT_SIZE),
            fill=COLOR_YELLOW
        )

        # イベント生成
        self.event = threading.Event()

        # マウスアクション登録
        canvas.tag_bind(self.text, '<Enter>', self._enter_start)
        canvas.tag_bind(self.text, '<Leave>', self._leave_start)
        canvas.tag_bind(self.text, '<ButtonPress-1>', self._on_start)

    def _enter_start(self, event):
        """
        カーソルが合った時
        """
        self.canvas.itemconfigure(self.text, fill=COLOR_RED)  # 赤色にする

    def _leave_start(self, event):
        """
        カーソルが離れた時
        """
        self.canvas.itemconfigure(self.text, fill=COLOR_YELLOW)  # 黄色にする

    def _on_start(self, event):
        """
        スタートテキストを押した場合
        """
        if not self.event.is_set():
            self.event.set()           # スタートイベントを通知

    def set_state(self, state):
        """
        スタートを有効化/無効化
        """
        text = START_TEXT if state == 'normal' else ''
        self.canvas.itemconfigure(self.text, text=text, state=state)


if __name__ == '__main__':
    import time
    from player import Player

    state = 'INIT'

    def resize_board(window):
        global state

        if window.menu.event.is_set():
            # メニューからの通知を取得
            window.size = window.menu.size
            window.player['black'] = window.menu.black_player
            window.player['white'] = window.menu.white_player
            window.assist = window.menu.assist

            state = 'INIT'  # ウィンドウ初期化
            window.menu.event.clear()   # イベントをクリア

            return True

        return False

    def demo_animation(window):
        center = window.board.size // 2

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
                if resize_board(window):
                    return False

                # アニメーション処理
                time.sleep(TURN_STONE_WAIT)
                window.board.remove_stone(remove_color, x, y)
                window.board.put_stone(put_color, x, y)

        return True

    def test_play(window, game_strategies):
        global state

        demo = False

        while True:
            resize_board(window)

            if state == 'INIT':
                demo = False
                window.init_screen()
                window.set_state('normal')
                state = 'DEMO'

            if state == 'DEMO':
                demo = True

                if window.start.event.is_set():
                    window.set_state('disable')  # メニューを無効化
                    window.start.event.clear()
                    state = 'START'
                else:
                    demo_animation(window)

            if state == 'START':
                if not demo:
                    window.init_screen()
                    window.set_state('disable')

                demo = False
                print('start', window.board.size, window.info.player['black'], window.info.player['white'])

                board = Board(window.board.size)
                black_player = Player('black', window.info.player['black'], game_strategies[window.info.player['black']])
                white_player = Player('white', window.info.player['white'], game_strategies[window.info.player['white']])

                while True:
                    playable = 0

                    moves = list(board.get_possibles('black').keys())

                    if moves:
                        window.board.enable_moves(moves)
                        window.board.selectable_moves(moves)

                        time.sleep(0.3)
                        black_player.put_stone(board)

                        window.board.disable_moves(moves)
                        window.board.enable_move(*black_player.move)

                        window.board.put_stone('black', *black_player.move)

                        time.sleep(0.3)
                        window.board.turn_stone('black', black_player.captures)

                        window.board.disable_move(*black_player.move)

                        playable += 1

                    moves = list(board.get_possibles('white').keys())

                    if moves:
                        window.board.enable_moves(moves)

                        time.sleep(0.3)
                        white_player.put_stone(board)

                        window.board.disable_moves(moves)
                        window.board.enable_move(*white_player.move)

                        window.board.put_stone('white', *white_player.move)

                        time.sleep(0.3)
                        window.board.turn_stone('white', white_player.captures)
                        window.board.disable_move(*white_player.move)

                        playable += 1

                    if not playable:
                        state = 'END'
                        window.set_state('normal')
                        break

            if state == 'END':
                demo = False

                if window.start.event.is_set():
                    window.set_state('disable')
                    window.start.event.clear()
                    state = 'START'

    root = tk.Tk()
    root.withdraw()  # 表示が整うまで隠す

    b = ['ユーザ', 'かんたん', 'ふつう', 'むずかしい']
    w = ['ユーザ', 'かんたん', 'ふつう', 'むずかしい']

    window = Window(root=root, black_players=b, white_players=w)

    game_strategies = {
        'ユーザ': strategies.WindowUserInput(window),
        'かんたん': strategies.Unselfish(),
        'ふつう': strategies.Random(),
        'むずかしい': strategies.Greedy(),
    }

    game = threading.Thread(target=test_play, args=([window, game_strategies]))
    game.daemon = True
    game.start()

    root.deiconify()  # 表示する
    root.mainloop()
