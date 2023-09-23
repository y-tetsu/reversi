"""GUIウィンドウ
"""
import os
import time
import tkinter as tk
import tkinter.filedialog as filedialog
import threading
import re

import reversi.board as board
import reversi.BitBoardMethods as BitBoardMethods
import reversi.strategies as strategies
import reversi.strategies.TableMethods as TableMethods
import reversi.strategies.AlphaBetaMethods as AlphaBetaMethods
import reversi.strategies.NegaScoutMethods as NegaScoutMethods

WINDOW_TITLE = 'reversi'  # ウィンドウのタイトル
WINDOW_WIDTH = 1320       # ウィンドウ幅
WINDOW_HEIGHT = 660       # ウィンドウ高さ

CANVAS_MERGINE = 4                              # キャンバスの余白
CANVAS_WIDTH = WINDOW_WIDTH - CANVAS_MERGINE    # キャンバスの幅
CANVAS_HEIGHT = WINDOW_HEIGHT - CANVAS_MERGINE  # キャンバスの高さ

COLOR_SLATEGRAY = 'slategray'  # スレートグレイ
COLOR_BLACK = 'black'          # 黒
COLOR_WHITE = 'white'          # 白
COLOR_LIGHTPINK = 'lightpink'  # ライトピンク
COLOR_GOLD = 'gold'            # ゴールド
COLOR_KHAKI = 'khaki2'         # カーキ
COLOR_TOMATO = 'tomato'        # トマト

INFO_OFFSET_X = {  # 表示テキストのXオフセット
    'black': WINDOW_WIDTH//7,
    'white': WINDOW_WIDTH-(WINDOW_WIDTH//7),
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
    'turn':    {'black': COLOR_LIGHTPINK, 'white': COLOR_LIGHTPINK},
    'move':    {'black': COLOR_BLACK,  'white': COLOR_WHITE},
}
INFO_FONT_SIZE = {  # 表示テキストのフォントサイズ
    'name':     32,
    'score':   140,
    'winlose':  32,
    'turn':     32,
    'move':     32,
}

START_OFFSET_X = WINDOW_WIDTH//2                # スタートのXオフセット
START_OFFSET_Y = 610                            # スタートのYオフセット
START_FONT_SIZE = 32                            # スタートのフォントサイズ

ASSIST_OFFSET_X = 20   # アシストのXオフセット
ASSIST_OFFSET_Y = 40   # アシストのYオフセット
ASSIST_FONT_SIZE = 12  # アシストのフォントサイズ

RECORD_OFFSET_X = 1270  # 棋譜出力のXオフセット
RECORD_OFFSET_Y = 40    # 棋譜出力のYオフセット
RECORD_FONT_SIZE = 12   # 棋譜出力のフォントサイズ

CPUTIME_OFFSET_X = 20   # CPUの持ち時間のXオフセット
CPUTIME_OFFSET_Y = 20   # CPUの持ち時間のYオフセット
CPUTIME_FONT_SIZE = 12  # CPUの持ち時間のフォントサイズ

SLOWMODE_OFFSET_X = 1290  # 低速モード表示のXオフセット
SLOWMODE_OFFSET_Y = 20    # 低速モード表示のYオフセット
SLOWMODE_FONT_SIZE = 12   # 低速モード表示のフォントサイズ

SQUAREHEADER_OFFSET_XY = 15  # マス目の列見出しのXYオフセット
SQUAREHEADER_FONT_SIZE = 20  # マス目の列見出しのフォントサイズ

SQUARE_OFFSET_Y = 40        # マス目のYオフセット
SQUARE_BOTTOM_MARGIN = 120  # マス目の底部のマージン
OVAL_SIZE_RATIO = 0.8       # マス目に対する石の円のサイズの割合
TURNOVAL_SIZE_DIVISOR = 10  # 石をひっくり返す途中のサイズ(マス目の何分の1か)

TURN_BLACK_PATTERN = [('white', 'turnwhite'), ('turnwhite', 'black')]  # 黒の石をひっくり返すパターン
TURN_WHITE_PATTERN = [('black', 'turnblack'), ('turnblack', 'white')]  # 白の石をひっくり返すパターン
TURN_DISC_WAIT = 0.1                                                   # 石をひっくり返す待ち時間(s)

ASSIST_MENU = ['ON', 'OFF']              # 打てる場所のハイライト表示の有無
RECORD_MENU = ['ON', 'OFF']              # 棋譜保存の有無
LANGUAGE_MENU = ['English', 'Japanese']  # 表示言語
CANCEL_MENU = ['OK']                     # ゲームのキャンセル

CPUTIME_MENU = ['Set']                         # CPUの持ち時間の変更
CPU_TIME = strategies.common.cputime.CPU_TIME  # CPUの持ち時間

EXTRA_MENU = ['Set']  # プレイヤー追加設定の変更

DISC_MARK = '●'      # 石のマーク

DEFAULT_BOARD_SIZE = 8   # ボードサイズの初期値
DEFAULT_BLACK_NUM = '2'  # 黒の石の数初期値
DEFAULT_WHITE_NUM = '2'  # 白の石の数初期値
DEFAULT_INFO_TEXT = {    # 表示テキストのテキスト初期値
    'name':    {'black': lambda s: DISC_MARK + s.player['black'], 'white': lambda s: DISC_MARK + s.player['white']},
    'score':   {'black': lambda s: '2',                           'white': lambda s: '2'},
    'winlose': {'black': lambda s: '',                            'white': lambda s: ''},
    'turn':    {'black': lambda s: '',                            'white': lambda s: ''},
    'move':    {'black': lambda s: '',                            'white': lambda s: ''},
}

CPUTIME_DIALOG_TITLE = 'CPU_TIME'  # タイトル
CPUTIME_DIALOG_WIDTH = 230         # 幅
CPUTIME_DIALOG_HEIGHT = 90         # 高さ

EXTRA_DIALOG_TITLE = 'Extra'  # タイトル
EXTRA_DIALOG_WIDTH = 700      # 幅
EXTRA_DIALOG_HEIGHT = 90      # 高さ

TEXTS = {
    LANGUAGE_MENU[0]: {                                                                # Engulish
        'START_TEXT': 'Click to start',                                                # Start Text
        'TURN_ON': 'Your turn',                                                        # Turn Display ON
        'TURN_OFF': '',                                                                # Turn Display OFF
        'MOVE_ON': '',                                                                 # Move Display ON
        'MOVE_OFF': '',                                                                # Move Display OFF
        'FOUL_ON': 'Foul',                                                             # Foul Display ON
        'WIN_ON': 'Win',                                                               # Win Display ON
        'LOSE_ON': 'Lose',                                                             # Lose Display ON
        'DRAW_ON': 'Draw',                                                             # Draw Display ON
        'CPU_WAIT_TEXT': 'Please set CPU wait time.',                                  # CPU wait time
        'CPU_SECOND_TEXT': '(sec)',                                                    # CPU wait time unit
        'CPU_SETTING_TEXT': 'Set',                                                     # CPU wait time setting
        'EXTRA_PLAYER_TEXT': 'Please add extra player by loading registration file.',  # Extra player
        'EXTRA_FILE_TEXT': 'Registration file',                                        # Registration file for Extra player
        'EXTRA_REF_TEXT': 'Reference',                                                 # Reference
        'EXTRA_LOAD_TEXT': 'Load',                                                     # Load
    },
    LANGUAGE_MENU[1]: {                                                           # Japanese
        'START_TEXT': 'クリックでスタート',                                       # スタートのテキスト
        'TURN_ON': '手番です',                                                    # 手番の表示ON
        'TURN_OFF': '',                                                           # 手番の表示OFF
        'MOVE_ON': ' に置きました',                                               # 手の表示ON
        'MOVE_OFF': '',                                                           # 手の表示OFF
        'FOUL_ON': '反則',                                                        # 反則負けの表示ON
        'WIN_ON': '勝ち',                                                         # 勝ちの表示ON
        'LOSE_ON': '負け',                                                        # 負けの表示ON
        'DRAW_ON': '引き分け',                                                    # 引き分けの表示ON
        'CPU_WAIT_TEXT': 'CPUの持ち時間を設定してください',                       # CPU待ち時間
        'CPU_SECOND_TEXT': '(秒)',                                                # CPU待ち時間の単位
        'CPU_SETTING_TEXT': '設定',                                               # CPU待ち時間の設定
        'EXTRA_PLAYER_TEXT': '登録ファイルを読み込むとプレイヤーを追加できます',  # 外部プレイヤー
        'EXTRA_FILE_TEXT': '登録ファイル',                                        # 登録ファイル
        'EXTRA_REF_TEXT': '参照',                                                 # 参照
        'EXTRA_LOAD_TEXT': '読み込む',                                            # 読み込む
    },
}


class Window(tk.Frame):
    """ウィンドウ
    """
    def __init__(self, root=None, black_players=None, white_players=None):
        super().__init__(root)
        self.pack()

        # 初期設定
        self.root = root
        self.size = DEFAULT_BOARD_SIZE
        self.player = {'black': black_players[0], 'white': white_players[0]}
        self.assist = ASSIST_MENU[1]
        self.record = RECORD_MENU[0]
        self.language = LANGUAGE_MENU[0]
        self.cancel = CANCEL_MENU[0]
        self.cputime = CPU_TIME
        self.extra_file = ''
        self.canvas_width = CANVAS_WIDTH
        self.canvas_height = CANVAS_HEIGHT
        self.pre_canvas_width = 0
        self.pre_canvas_height = 0
        self.canvas_width_hist = [self.pre_canvas_width, self.canvas_width]
        self.canvas_height_hist = [self.pre_canvas_height, self.canvas_height]

        # ウィンドウ設定
        self.root.title(WINDOW_TITLE)                       # タイトル
        self.root.minsize(WINDOW_WIDTH-100, WINDOW_HEIGHT)  # 最小サイズ

        # メニューを配置
        self.menu = Menu(self, black_players, white_players)
        root.configure(menu=self.menu)

        # キャンバスを配置
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg=COLOR_SLATEGRAY)
        self.canvas.grid(row=0, column=0)

        # 表示サイズと位置
        x_offset = (root.winfo_screenwidth() // 2) - (WINDOW_WIDTH // 2)
        y_offset = (root.winfo_screenheight() // 2) - (WINDOW_HEIGHT // 2)
        width = WINDOW_WIDTH
        height = WINDOW_HEIGHT
        self.root.geometry(f'{width}x{height}+{x_offset}+{y_offset}')

    def init_screen(self):
        """ゲーム画面の初期化
        """
        self.canvas.delete('all')                                                                                                        # 全オブジェクト削除
        self.board = ScreenBoard(self.canvas, self.size, self.cputime, self.assist, self.record, self.canvas_width, self.canvas_height)  # ボード配置
        self.info = ScreenInfo(self.canvas, self.player, self.language, self.canvas_width)                                               # 情報表示テキスト配置
        self.start = ScreenStart(self.canvas, self.language, self.canvas_width, self.canvas_height)                                      # スタートテキスト配置

        # ウィンドウサイズ変更時のイベントをバインド
        self.root.bind("<Configure>", self.on_resize)

    def set_state(self, state):
        """ウィンドウを有効化/無効化
        """
        self.start.set_state(state)
        self.menu.set_state(state)

    def on_resize(self, event):
        """ウィンドウサイズ変更時の処理
        """
        self.canvas_width_hist.pop(0)
        self.canvas_width_hist.append(event.width-CANVAS_MERGINE)

        self.canvas_height_hist.pop(0)
        self.canvas_height_hist.append(event.height-CANVAS_MERGINE)

        canvas_width = max(self.canvas_width_hist)
        canvas_height = max(self.canvas_height_hist)

        # ウィンドウサイズ変更時
        if canvas_width != self.pre_canvas_width or canvas_height != self.pre_canvas_height:
            self.canvas_width = canvas_width
            self.canvas_height = canvas_height

            self.board.canvas_width = canvas_width
            self.board.canvas_height = canvas_height

            # スクリーンを更新
            area_size = max(min(canvas_width//2, canvas_height), CANVAS_HEIGHT)
            area_ratio = area_size / CANVAS_HEIGHT
            offset = (area_size - CANVAS_HEIGHT)/4
            self.board.area_ratio = area_ratio
            self.board.offset = offset
            self.update_screen(canvas_width, canvas_height, area_ratio, offset)

        self.pre_canvas_width = canvas_width
        self.pre_canvas_height = canvas_height

    def update_screen(self, canvas_width, canvas_height, area_ratio, offset):
        """スクリーンを更新する
        """
        dw = canvas_width - CANVAS_WIDTH
        dwc = dw // 2
        dh = canvas_height - CANVAS_HEIGHT
        dhc = dh // 2

        # キャンバスサイズ
        self.canvas.configure(width=canvas_width, height=canvas_height)

        # WHITE-INFO
        for name in INFO_OFFSET_Y:
            text = self.info.text['white_' + name]
            x = (canvas_width+CANVAS_MERGINE)-(WINDOW_WIDTH//7)
            y = INFO_OFFSET_Y[name]
            self.canvas.coords(text, x, y)

        # RECORD
        self.canvas.coords(self.board.record_text, RECORD_OFFSET_X+dw, RECORD_OFFSET_Y)

        # SLOWMODE
        if BitBoardMethods.SLOW_MODE1 or BitBoardMethods.SLOW_MODE2 or BitBoardMethods.SLOW_MODE3 or BitBoardMethods.SLOW_MODE4 or BitBoardMethods.SLOW_MODE5 or TableMethods.SLOW_MODE or AlphaBetaMethods.SLOW_MODE or NegaScoutMethods.SLOW_MODE or BitBoardMethods.CYBOARD_ERROR:  # noqa: E501
            self.canvas.coords(self.board.slowmode_text, SLOWMODE_OFFSET_X+dw, SLOWMODE_OFFSET_Y)

        # START
        self.canvas.coords(self.start.text, START_OFFSET_X+dwc+offset/2, START_OFFSET_Y+dhc+offset*2)

        # SQUARES
        square_w = self.board.square_w * area_ratio
        min_x, min_y = self.board.square_x_ini-offset, self.board.square_y_ini-offset
        max_x, max_y = min_x + square_w * self.size, min_y + square_w * self.size
        row_x, col_y = min_x - SQUAREHEADER_OFFSET_XY, min_y - SQUAREHEADER_OFFSET_XY
        # - x lines
        for num, xline in enumerate(self.board._xlines):
            square_x1, square_y1 = min_x, min_y + square_w * num
            square_x2, square_y2 = max_x, square_y1
            self.canvas.coords(xline, square_x1+dwc, square_y1+dhc, square_x2+dwc, square_y2+dhc)
        # - y lines
        for num, yline in enumerate(self.board._ylines):
            square_x1, square_y1 = min_x + square_w * num, min_y
            square_x2, square_y2 = square_x1, max_y
            self.canvas.coords(yline, square_x1+dwc, square_y1+dhc, square_x2+dwc, square_y2+dhc)
        # - alphabet texts
        for num, atext in enumerate(self.board._atexts):
            text_x, text_y = (min_x + square_w * num) + square_w // 2, col_y
            self.canvas.coords(atext, text_x+dwc, text_y+dhc)
        # - number texts
        for num, ntext in enumerate(self.board._ntexts):
            text_x, text_y = row_x, (min_y + square_w * num) + square_w // 2
            self.canvas.coords(ntext, text_x+dwc, text_y+dhc)
        # - 4x4 circle
        if self.size > 4:
            num = self.size//2 + 2
            mark_w = int(square_w * OVAL_SIZE_RATIO * 0.2)
            index = 0
            for x_offset in [square_w * (num - 4), square_w * num]:
                for y_offset in [square_w * (num - 4), square_w * num]:
                    mark_x1, mark_y1 = min_x + x_offset - mark_w//2, min_y + y_offset - mark_w//2
                    mark_x2, mark_y2 = min_x + x_offset + mark_w//2, min_y + y_offset + mark_w//2
                    self.canvas.coords(self.board._4x4circle[index], mark_x1+dwc, mark_y1+dhc, mark_x2+dwc, mark_y2+dhc)
                    index += 1
        # - discs
        for (label, color, index_x, index_y), disc in self.board._discs.items():
            x, y = self.board._get_coordinate(index_x, index_y)
            if color == 'black' or color == 'white':
                w = self.board.oval_w1 * area_ratio
                x1, y1, x2, y2 = x - w/2, y - w/2, x + w/2, y + w/2
                self.canvas.coords(disc, x1, y1, x2, y2)
            else:
                w1, w2 = self.board.oval_w1*area_ratio, self.board.oval_w2*area_ratio
                x1, y1, x2, y2 = x - w2, y - w1/2, x, y + w1/2
                x3, x4 = x, x + w2
                if color.endswith('1'):
                    self.canvas.coords(disc, x1, y1, x2, y2)
                else:
                    self.canvas.coords(disc, x3, y1, x4, y2)
        # - moves
        for y in range(self.size):
            for x in range(self.size):
                square = self.board._squares[y][x]
                try:
                    x1 = min_x + square_w * x
                    x2 = x1 + square_w
                    y1 = min_y + square_w * y
                    y2 = y1 + square_w
                    self.canvas.coords(square, x1+dwc, y1+dhc, x2+dwc, y2+dhc)
                except ValueError:
                    pass
                except tk._tkinter.TclError:
                    pass


class Menu(tk.Menu):
    """メニュー
    """
    def __init__(self, window, black_players, white_players):
        super().__init__(window.root)

        self.window = window
        self.size = DEFAULT_BOARD_SIZE
        self.black_player = black_players[0]
        self.white_player = white_players[0]
        self.assist = ASSIST_MENU[1]
        self.record = RECORD_MENU[0]
        self.language = LANGUAGE_MENU[0]
        self.cancel = CANCEL_MENU[0]
        self.menu_items = {}
        self.cputimedialog = None
        self.extradialog = None

        # イベントの生成
        self.event = threading.Event()

        # メニューアイテムの生成
        self.menu_items['size'] = range(board.MIN_BOARD_SIZE, board.MAX_BOARD_SIZE + 1, 2)
        self.menu_items['black'] = black_players
        self.menu_items['white'] = white_players
        self.menu_items['cputime'] = CPUTIME_MENU
        self.menu_items['extra'] = EXTRA_MENU
        self.menu_items['assist'] = ASSIST_MENU
        self.menu_items['record'] = RECORD_MENU
        self.menu_items['language'] = LANGUAGE_MENU
        self.menu_items['cancel'] = CANCEL_MENU
        self._create_menu_items()

    def _create_menu_items(self):
        """メニューの追加
        """
        self.menus = {}

        for name, items in self.menu_items.items():
            menu = tk.Menu(self, tearoff=False)
            self.menus[name] = menu

            for item in items:
                menu.add_command(label=str(item), command=self._command(name, item))

            self.add_cascade(menu=menu, label=name.title())

    def _command(self, name, item):
        """メニュー設定変更時
        """
        def change_menu_selection():
            if not self.event.is_set():
                self.size = item if name == 'size' else self.size
                self.black_player = item if name == 'black' else self.black_player
                self.white_player = item if name == 'white' else self.white_player

                if name == 'cputime':
                    self.cputimedialog = CpuTimeDialog(window=self.window, event=self.event, language=self.language)

                if name == 'extra':
                    self.extradialog = ExtraDialog(window=self.window, event=self.event, language=self.language)

                self.assist = item if name == 'assist' else self.assist
                self.record = item if name == 'record' else self.record
                self.language = item if name == 'language' else self.language
                self.cancel = item if name == 'cancel' else self.cancel
                self.event.set()  # ウィンドウへメニューの設定変更を通知

        return change_menu_selection

    def set_state(self, state):
        """メニューのステータス設定(有効化/無効化)
        """
        for name in self.menu_items.keys():
            if name == 'cancel':
                state = 'normal' if state == 'disable' else 'disable'
            self.entryconfigure(name.title(), state=state)


class CpuTimeDialog:
    """CPUの持ち時間設定ダイアログ
    """
    def __init__(self, window=None, event=None, language=None):
        self.window = window
        self.event = event
        self.dialog = tk.Toplevel(master=self.window.root)
        self.dialog.title(CPUTIME_DIALOG_TITLE)
        self.dialog.minsize(CPUTIME_DIALOG_WIDTH, CPUTIME_DIALOG_HEIGHT)  # 最小サイズ
        self.dialog.resizable(1, 0)  # 横方向だけリサイズ許可
        self.dialog.grab_set()

        self.parameter = tk.StringVar()
        self.parameter.set(self.window.cputime)
        self.label1 = tk.Label(self.dialog, text=TEXTS[language]['CPU_WAIT_TEXT'])
        self.label1.pack(anchor='w')

        frame = tk.Frame(self.dialog)
        frame.pack(fill='x', pady='5')
        label = tk.Label(frame, text='')
        label.pack(side='left', padx='5')
        self.entry = tk.Entry(frame, textvariable=self.parameter)
        self.entry.pack(side='left', expand=1, fill='x', pady='5')
        self.label2 = tk.Label(frame, text=TEXTS[language]['CPU_SECOND_TEXT'])
        self.label2.pack(side='right', padx='5')

        self.button = tk.Button(self.dialog, text=TEXTS[language]['CPU_SETTING_TEXT'], command=self.set_parameter)
        self.button.pack()

    def set_parameter(self):
        """パラメータを設定する
        """
        value = self.parameter.get()
        # 入力値が数値である
        if re.match(r'\d+(?:\.\d+)?', value) is not None:
            # 0より大きい
            float_value = float(value)
            if float_value > 0:
                self.window.cputime = float_value
                self.event.set()  # ウィンドウへメニューの設定変更を通知
                self.dialog.destroy()


class ExtraDialog:
    """Extra設定ダイアログ
    """
    def __init__(self, window=None, event=None, language=None):
        self.window = window
        self.event = event
        self.askopenfilename = filedialog.askopenfilename
        self.dialog = tk.Toplevel(master=self.window.root)
        self.dialog.title(EXTRA_DIALOG_TITLE)
        self.dialog.minsize(EXTRA_DIALOG_WIDTH, EXTRA_DIALOG_HEIGHT)  # 最小サイズ
        self.dialog.resizable(1, 0)  # 横方向だけリサイズ許可
        self.dialog.grab_set()

        self.extra_file = tk.StringVar()
        self.extra_file.set(self.window.extra_file)
        self.label1 = tk.Label(self.dialog, text=TEXTS[language]['EXTRA_PLAYER_TEXT'])
        self.label1.pack(anchor='w', padx='5')

        frame = tk.Frame(self.dialog)
        frame.pack(fill='x', pady='5')
        self.label2 = tk.Label(frame, text=TEXTS[language]['EXTRA_FILE_TEXT'])
        self.label2.pack(side='left', padx='5')

        self.entry = tk.Entry(frame, textvariable=self.extra_file)
        self.entry.pack(side='left', expand=1, fill='x', pady='5')

        self.button1 = tk.Button(frame, text=TEXTS[language]['EXTRA_REF_TEXT'], command=self.select_extra_file)
        self.button1.pack(side='right', padx='5')

        self.button2 = tk.Button(self.dialog, text=TEXTS[language]['EXTRA_LOAD_TEXT'], command=self.set_parameter)
        self.button2.pack()

    def select_extra_file(self):
        """登録ファイルを選択する
        """
        ini_dir = os.path.abspath(os.path.dirname('./extra/'))
        extra_file = self.askopenfilename(filetypes=[("", "*.json")], initialdir=ini_dir)
        if extra_file:
            self.extra_file.set(extra_file)

    def set_parameter(self):
        """パラメータを設定する
        """
        extra_file = self.extra_file.get()
        self.window.extra_file = extra_file
        self.event.set()  # ウィンドウへメニューの設定変更を通知
        self.dialog.destroy()


class ScreenBoard:
    """ボードの表示
    """
    def __init__(self, canvas, size, cputime, assist, record, canvas_width=CANVAS_WIDTH, canvas_height=CANVAS_HEIGHT):
        self.size = size
        self.cputime = cputime
        self.assist = assist
        self.record = record
        self.canvas = canvas
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self._squares = []
        self._xlines = []
        self._ylines = []
        self._atexts = []
        self._ntexts = []
        self._4x4circle = []
        self._discs = {}
        self.move = None

        area_size = max(min(canvas_width//2, canvas_height), CANVAS_HEIGHT)
        self.area_ratio = area_size / CANVAS_HEIGHT
        self.offset = (area_size - CANVAS_HEIGHT)/4

        dw = canvas_width - CANVAS_WIDTH

        # イベント生成
        self.event = threading.Event()

        # CPUの持ち時間表示
        cputime_text = 'CPU_TIME(' + str(self.cputime) + 's)'
        self.canvas.create_text(
            CPUTIME_OFFSET_X,
            CPUTIME_OFFSET_Y,
            text=cputime_text,
            font=('', CPUTIME_FONT_SIZE),
            anchor='w',
            fill=COLOR_WHITE
        )

        # アシスト表示
        assist_text = 'Assist On' if self.assist == 'ON' else ''
        self.canvas.create_text(
            ASSIST_OFFSET_X,
            ASSIST_OFFSET_Y,
            text=assist_text,
            font=('', ASSIST_FONT_SIZE),
            anchor='w',
            fill=COLOR_WHITE
        )

        # 棋譜出力表示
        record_text = 'REC' if self.record == 'ON' else ''
        self.record_text = self.canvas.create_text(
            RECORD_OFFSET_X+dw,
            RECORD_OFFSET_Y,
            text=record_text,
            font=('', RECORD_FONT_SIZE),
            anchor='w',
            fill=COLOR_TOMATO
        )

        # 低速モードの表示
        slowmode_text = '■'
        if BitBoardMethods.SLOW_MODE1 or BitBoardMethods.SLOW_MODE2 or BitBoardMethods.SLOW_MODE3 or BitBoardMethods.SLOW_MODE4 or BitBoardMethods.SLOW_MODE5 or TableMethods.SLOW_MODE or AlphaBetaMethods.SLOW_MODE or NegaScoutMethods.SLOW_MODE or BitBoardMethods.CYBOARD_ERROR:  # noqa: E501
            self.slowmode_text = self.canvas.create_text(
                SLOWMODE_OFFSET_X+dw,
                SLOWMODE_OFFSET_Y,
                text=slowmode_text,
                font=('', SLOWMODE_FONT_SIZE),
                anchor='w',
                fill=COLOR_TOMATO
            )

        # ボードの描画
        self._draw_squares()

    def _draw_squares(self):
        """マス目を描画
        """
        dw = self.canvas_width - CANVAS_WIDTH
        dwc = dw // 2
        dh = self.canvas_height - CANVAS_HEIGHT
        dhc = dh // 2

        size = self.size
        self._squares = [[None for _ in range(size)] for _ in range(size)]

        # マス目や石のサイズを計算
        self.square_y_ini = SQUARE_OFFSET_Y
        self.square_w = (WINDOW_HEIGHT - self.square_y_ini - SQUARE_BOTTOM_MARGIN) // size
        w = self.square_w * self.area_ratio
        self.square_x_ini = CANVAS_WIDTH // 2 - (self.square_w * size) // 2
        self.oval_w1 = int(self.square_w * OVAL_SIZE_RATIO)
        self.oval_w2 = int(self.square_w // TURNOVAL_SIZE_DIVISOR)

        # マス目や見出しの位置を初期化
        min_x, min_y = self.square_x_ini-self.offset, self.square_y_ini-self.offset
        max_x, max_y = min_x + w * size, min_y + w * size
        row_x, col_y = min_x - SQUAREHEADER_OFFSET_XY, min_y - SQUAREHEADER_OFFSET_XY
        label = None
        text_x, text_y = None, None
        square_x1, square_y1, square_x2, square_y2 = None, None, None, None
        line_append, xappend, yappend = None, self._xlines.append, self._ylines.append
        text_append, aappend, nappend = None, self._atexts.append, self._ntexts.append

        # マス目の描画
        for num in range(size + 1):
            for rc in ('row', 'col'):
                if rc == 'row':
                    label = str(num + 1)
                    text_x, text_y = row_x, (min_y + w * num) + w // 2
                    square_x1, square_y1 = min_x + w * num, min_y
                    square_x2, square_y2 = square_x1, max_y
                    line_append = yappend
                    text_append = nappend
                else:
                    label = chr(num + 97)
                    text_x, text_y = (min_x + w * num) + w // 2, col_y
                    square_x1, square_y1 = min_x, min_y + w * num
                    square_x2, square_y2 = max_x, square_y1
                    line_append = xappend
                    text_append = aappend

                # 番地
                if num < size:
                    text = self.canvas.create_text(text_x+dwc, text_y+dhc, fill=COLOR_WHITE, text=label, font=('', SQUAREHEADER_FONT_SIZE))
                    text_append(text)

                # マス目の線
                line = self.canvas.create_line(square_x1+dwc, square_y1+dhc, square_x2+dwc, square_y2+dhc, fill=COLOR_WHITE)
                line_append(line)

            # 目印の描画
            if size > 4 and num == size//2 + 2:
                mark_w = int(w * OVAL_SIZE_RATIO * 0.2)
                for x_offset in [w * (num - 4), w * num]:
                    for y_offset in [w * (num - 4), w * num]:
                        mark_x1, mark_y1 = min_x + x_offset - mark_w//2, min_y + y_offset - mark_w//2
                        mark_x2, mark_y2 = min_x + x_offset + mark_w//2, min_y + y_offset + mark_w//2
                        oval = self.canvas.create_oval(mark_x1+dwc, mark_y1+dhc, mark_x2+dwc, mark_y2+dhc, tag='mark', fill=COLOR_WHITE, outline=COLOR_WHITE)
                        self._4x4circle.append(oval)

        # 初期位置に石を置く
        center = size // 2
        self.put_disc('black', center, center-1)
        self.put_disc('black', center-1, center)
        self.put_disc('white', center-1, center-1)
        self.put_disc('white', center, center)

    def put_disc(self, color, index_x, index_y):
        """石を置く
        """
        x, y = self._get_coordinate(index_x, index_y)

        # 黒か白の石をおく
        if color == 'black' or color == 'white':
            w = self.oval_w1 * self.area_ratio
            x1, y1, x2, y2 = x - w/2, y - w/2, x + w/2, y + w/2
            label = self._get_label(color, index_x, index_y)
            oval = self.canvas.create_oval(x1, y1, x2, y2, tag=label, fill=color, outline=color)
            self._discs[(label, color, index_x, index_y)] = oval

        # ひっくり返す途中
        else:
            w1, w2 = self.oval_w1 * self.area_ratio, self.oval_w2 * self.area_ratio
            label1 = self._get_label(color + '1', index_x, index_y)
            label2 = self._get_label(color + '2', index_x, index_y)
            color1 = 'white' if color == 'turnblack' else 'black'
            color2 = 'black' if color == 'turnblack' else 'white'

            x1, y1, x2, y2 = x - w2, y - w1/2, x, y + w1/2
            rect1 = self.canvas.create_rectangle(x1, y1, x2, y2, tag=label1, fill=color1, outline=color1)
            x3, x4 = x, x + w2
            rect2 = self.canvas.create_rectangle(x3, y1, x4, y2, tag=label2, fill=color2, outline=color2)

            self._discs[(label1, color + '1', index_x, index_y)] = rect1
            self._discs[(label2, color + '2', index_x, index_y)] = rect2

    def remove_disc(self, color, index_x, index_y):
        """石を消す
        """
        ptns = []
        if color == 'black' or color == 'white':
            ptns = [color]
        else:
            ptns = [color + str(i) for i in range(1, 3)]

        for ptn in ptns:
            label = self._get_label(ptn, index_x, index_y)
            self.canvas.delete(label)
            key = (label, color, index_x, index_y)
            if key in self._discs:
                del self._discs[key]

    def _get_coordinate(self, index_x, index_y):
        """座標を計算する
        """
        x_ini = self.square_x_ini - self.offset
        y_ini = self.square_y_ini - self.offset
        w = self.square_w * self.area_ratio
        dw = (self.canvas_width - CANVAS_WIDTH)//2
        dh = (self.canvas_height - CANVAS_HEIGHT)//2
        return x_ini + w * index_x + w // 2 + dw, y_ini + w * index_y + w // 2 + dh

    def _get_label(self, name, x, y):
        """表示ラベルを返す
        """
        return name + '_' + chr(x + 97) + str(y + 1)

    def turn_disc(self, color, captures):
        """石をひっくり返す
        """
        ptn = TURN_BLACK_PATTERN if color == 'black' else TURN_WHITE_PATTERN

        for remove_color, put_color in ptn:
            for x, y in captures:
                self.remove_disc(remove_color, x, y)
            for x, y in captures:
                self.put_disc(put_color, x, y)
            time.sleep(TURN_DISC_WAIT)

    def enable_moves(self, moves):
        """打てる場所をハイライトする
        """
        square_w = self.square_w * self.area_ratio

        dw = (self.canvas_width - CANVAS_WIDTH)//2
        dh = (self.canvas_height - CANVAS_HEIGHT)//2
        for x, y in moves:
            x1 = self.square_x_ini + square_w * x - self.offset
            x2 = x1 + square_w
            y1 = self.square_y_ini + square_w * y - self.offset
            y2 = y1 + square_w
            if self.assist == 'ON':
                self._squares[y][x] = self.canvas.create_rectangle(x1+dw, y1+dh, x2+dw, y2+dh, fill=COLOR_KHAKI, outline=COLOR_WHITE, tag='moves')
            else:
                self._squares[y][x] = self.canvas.create_rectangle(x1+dw, y1+dh, x2+dw, y2+dh, fill=COLOR_SLATEGRAY, outline=COLOR_WHITE, tag='moves')
        self.canvas.tag_raise('mark', 'moves')

    def disable_moves(self, moves):
        """打てる場所のハイライトを元に戻す
        """
        self.canvas.delete('moves')

    def enable_move(self, x, y):
        """打った場所をハイライトする
        """
        square_w = self.square_w * self.area_ratio

        dw = (self.canvas_width - CANVAS_WIDTH)//2
        dh = (self.canvas_height - CANVAS_HEIGHT)//2
        x1 = self.square_x_ini + square_w * x - self.offset
        x2 = x1 + square_w
        y1 = self.square_y_ini + square_w * y - self.offset
        y2 = y1 + square_w
        self._squares[y][x] = self.canvas.create_rectangle(x1+dw, y1+dh, x2+dw, y2+dh, fill=COLOR_TOMATO, outline=COLOR_WHITE, tag='move')
        self.canvas.tag_raise('mark', 'move')

    def disable_move(self, x, y):
        """打った場所のハイライトを元に戻す
        """
        self.canvas.delete('move')

    def selectable_moves(self, moves):
        """打てる場所を選択できるようにする
        """
        for x, y in moves:
            square = self._squares[y][x]
            self.canvas.tag_bind(square, '<Enter>', self._enter_selectable_moves(square))
            self.canvas.tag_bind(square, '<Leave>', self._leave_selectable_moves(square))
            self.canvas.tag_bind(square, '<ButtonPress-1>', self._press_selectable_moves(x, y))

    def unselectable_moves(self, moves):
        """打てる場所を選択できないようにする
        """
        for x, y in moves:
            square = self._squares[y][x]
            self.canvas.tag_bind(square, '<Enter>', lambda *args: None)
            self.canvas.tag_bind(square, '<Leave>', lambda *args: None)
            self.canvas.tag_bind(square, '<ButtonPress-1>', lambda *args: None)

    def _enter_selectable_moves(self, square):
        """打てる場所にカーソルが合ったとき
        """
        def _enter(event):
            if self.assist == 'ON':
                self.canvas.itemconfigure(square, fill=COLOR_TOMATO)
        return _enter

    def _leave_selectable_moves(self, square):
        """打てる場所からカーソルが離れた
        """
        def _leave(event):
            if self.assist == 'ON':
                self.canvas.itemconfigure(square, fill=COLOR_KHAKI)
        return _leave

    def _press_selectable_moves(self, x, y):
        """打てる場所をクリックしたとき
        """
        def _press(event):
            if not self.event.is_set():
                self.move = (x, y)
                self.event.set()  # ウィンドウへ手の選択を通知
        return _press


class ScreenInfo:
    """情報表示テキスト
    """
    def __init__(self, canvas, player, language, canvas_width=CANVAS_WIDTH):
        self.canvas = canvas
        self.player = player
        self.language = language
        self.canvas_width = canvas_width
        self.text = {}

        # テキスト作成
        for name in INFO_OFFSET_Y.keys():
            for color in INFO_OFFSET_X.keys():
                self._create_text(color, name)  # 表示テキスト

    def _create_text(self, color, name):
        """表示テキスト作成
        """
        offset_x = INFO_OFFSET_X[color]
        if color == 'white':
            offset_x = (self.canvas_width+CANVAS_MERGINE)-(WINDOW_WIDTH//7)

        self.text[color + '_' + name] = self.canvas.create_text(
            offset_x,
            INFO_OFFSET_Y[name],
            text=DEFAULT_INFO_TEXT[name][color](self),
            font=('', INFO_FONT_SIZE[name]),
            fill=INFO_COLOR[name][color]
        )

    def set_text(self, color, name, text):
        """表示テキストの文字列を設定
        """
        text_id = self.text[color + '_' + name]
        self.canvas.itemconfigure(text_id, text=text)

    def set_turn_text_on(self, color):
        """手番を表示
        """
        text_id = self.text[color + '_' + 'turn']
        self.canvas.itemconfigure(text_id, text=TEXTS[self.language]['TURN_ON'])

    def set_turn_text_off(self, color):
        """手番を表示
        """
        text_id = self.text[color + '_' + 'turn']
        self.canvas.itemconfigure(text_id, text=TEXTS[self.language]['TURN_OFF'])

    def set_move_text_on(self, color, x, y):
        """手を表示
        """
        text_id = self.text[color + '_' + 'move']
        self.canvas.itemconfigure(text_id, text=f'({x}, {y})' + TEXTS[self.language]['MOVE_ON'])

    def set_move_text_off(self, color):
        """手を表示
        """
        text_id = self.text[color + '_' + 'move']
        self.canvas.itemconfigure(text_id, text=TEXTS[self.language]['MOVE_OFF'])

    def set_foul_text_on(self, color):
        """反則負けを表示
        """
        text_id = self.text[color + '_' + 'winlose']
        self.canvas.itemconfigure(text_id, text=TEXTS[self.language]['FOUL_ON'])

    def set_win_text_on(self, color):
        """勝ちを表示
        """
        text_id = self.text[color + '_' + 'winlose']
        self.canvas.itemconfigure(text_id, text=TEXTS[self.language]['WIN_ON'])

    def set_lose_text_on(self, color):
        """負けを表示
        """
        text_id = self.text[color + '_' + 'winlose']
        self.canvas.itemconfigure(text_id, text=TEXTS[self.language]['LOSE_ON'])

    def set_draw_text_on(self, color):
        """引き分けを表示
        """
        text_id = self.text[color + '_' + 'winlose']
        self.canvas.itemconfigure(text_id, text=TEXTS[self.language]['DRAW_ON'])


class ScreenStart:
    """スタートテキスト
    """
    def __init__(self, canvas, language, canvas_width=CANVAS_WIDTH, canvas_height=CANVAS_HEIGHT):
        self.canvas = canvas
        self.language = language

        area_size = max(min(canvas_width//2, canvas_height), CANVAS_HEIGHT)
        offset = (area_size - CANVAS_HEIGHT)/4

        # テキスト作成
        dw = canvas_width - CANVAS_WIDTH
        dwc = dw // 2
        dh = canvas_height - CANVAS_HEIGHT
        dhc = dh // 2
        self.text = canvas.create_text(
            START_OFFSET_X+dwc+offset/2,
            START_OFFSET_Y+dhc+offset*2,
            text=TEXTS[self.language]['START_TEXT'],
            font=('', START_FONT_SIZE),
            fill=COLOR_GOLD
        )

        # イベント生成
        self.event = threading.Event()

        # マウスアクション登録
        canvas.tag_bind(self.text, '<Enter>', self._enter_start)
        canvas.tag_bind(self.text, '<Leave>', self._leave_start)
        canvas.tag_bind(self.text, '<ButtonPress-1>', self._on_start)

    def _enter_start(self, event):
        """カーソルが合った時
        """
        self.canvas.itemconfigure(self.text, fill=COLOR_TOMATO)

    def _leave_start(self, event):
        """カーソルが離れた時
        """
        self.canvas.itemconfigure(self.text, fill=COLOR_GOLD)

    def _on_start(self, event):
        """スタートテキストを押した場合
        """
        if not self.event.is_set():
            self.event.set()  # スタートイベントを通知

    def set_state(self, state):
        """スタートを有効化/無効化
        """
        text = TEXTS[self.language]['START_TEXT'] if state == 'normal' else ''
        self.canvas.itemconfigure(self.text, text=text, state=state)
