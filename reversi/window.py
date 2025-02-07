"""GUIウィンドウ
"""
import os
import time
import tkinter as tk
import tkinter.filedialog as filedialog
import threading
import re

import reversi.board as board
import reversi.cy as cy

from reversi.strategies import CPU_TIME


WINDOW_TITLE = 'reversi'  # ウィンドウのタイトル
WINDOW_WIDTH = 1320       # ウィンドウ幅
WINDOW_HEIGHT = 660       # ウィンドウ高さ

CANVAS_MERGINE = 4                              # キャンバスの余白
CANVAS_WIDTH = WINDOW_WIDTH - CANVAS_MERGINE    # キャンバスの幅
CANVAS_HEIGHT = WINDOW_HEIGHT - CANVAS_MERGINE  # キャンバスの高さ

COLOR_BACKGROUND = 'slategray'    # 背景
COLOR_BOARD = 'slategray'         # 盤面
COLOR_PLAYER1_LABEL = 'black'     # 先手表示
COLOR_PLAYER2_LABEL = 'white'     # 後手表示
COLOR_PLAYER1_DISC = 'black'      # 先手石
COLOR_PLAYER2_DISC = 'white'      # 後手石
COLOR_CPUTIME_LABEL = 'white'     # CPU_TIMEラベル
COLOR_ASSIST_LABEL = 'white'      # ASSISTラベル
COLOR_CELL_NUMBER = 'white'       # セル番地
COLOR_CELL_LINE = 'white'         # セルの枠線
COLOR_CELL_MARK = 'white'         # セルの目印
COLOR_TURN_MESSAGE = 'lightpink'  # 手番表示
COLOR_START_MESSAGE1 = 'gold'     # スタート表示(フォーカスなし)
COLOR_START_MESSAGE2 = 'tomato'   # スタート表示(フォーカスあり)
COLOR_MOVE_HIGHLIGHT1 = 'khaki2'  # 着手箇所のハイライト(フォーカスなし)
COLOR_MOVE_HIGHLIGHT2 = 'tomato'  # 着手箇所のハイライト(フォーカスあり)
COLOR_REC_LABEL = 'tomato'        # レコーディング表示
COLOR_LOWSPEED_LABEL = 'tomato'   # 低速表示

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
    'name':    {'black': COLOR_PLAYER1_LABEL,  'white': COLOR_PLAYER2_LABEL},
    'score':   {'black': COLOR_PLAYER1_LABEL,  'white': COLOR_PLAYER2_LABEL},
    'winlose': {'black': COLOR_PLAYER1_LABEL,  'white': COLOR_PLAYER2_LABEL},
    'turn':    {'black': COLOR_TURN_MESSAGE, 'white': COLOR_TURN_MESSAGE},
    'move':    {'black': COLOR_PLAYER1_LABEL,  'white': COLOR_PLAYER2_LABEL},
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

ICON = """
R0lGODlhAAIAAveRAAAAAAAAAAkGAg4KBBMNBRcQBhkRBx0TCCEXCSUZCyodDC8g
DTMjDjcmEDknEDwpEUEsEkYwFE40FlA2FlI4F1U5GFo9GV9AG2NDHGlHHm1KH3RO
IXdRIn1VI41uB4FmCIRpCIlrCI9wB5N0CZx7CaJ/CoFXJIVaJotfJ41fKI5gKJNk
KZlnK51rLKNuLqVwL6hyL6x0MLB3MrR6M7p+NKOBCa6ICrOOCriSCr2BNcWbC8yh
C9aoDNytDOS0De26DfG+DcOEN8eHOMiHOMyLOtKOO9WRPNyVPt+YP+GZP/XBDfrF
Dv/JDuOaQOmeQu6hQ/SmRfeoRvyrR/ytS/yvUPyxVPy1XPy3Yfy5ZP27av2/cv/W
SNvCbefMbv/fb/3Adv3Ceo+Pj9PFk9zMlP3Ggv3Ihv3JiP3OlP3Ql/3Sm//nlv7W
pv7XqP7Yqv7dtP7fuf7hvf7kxf7myP7ozf7r0/7u2/7w3f7w3/7w3//x4f/y4//y
4v/z5f/z5P/05//z5P/16P/16f/26//37f/27P/37v/27P/47//48P/58f/58v/6
8//69f/79v/69f/9+v/8+f/////+/v/+/P///wAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAACH5BAEAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1
NQAsAAAAAAACAAIACP8AAQgcSLCgwYMIEypcyLChw4cQI0qcSLGixYsYM2rcyLGj
x48gQ4ocSbKkyZMoU6pcybKly5cwY8qcSbOmzZs4c+rcybOnz59AgwodSrSo0aNI
kypdyrSp06dQo0qdSrWq1atYs2rdyrWr169gHd7AQbas2bNo06pdy7at27dw48qd
S7eu3bt48+rdy7cv2xphMd5gQriw4cOIEytezLix48eQI0ueTLmy5cuYM2vezLlz
4yWAA1O8scSz6dOoU6tezbq169edQYuOSEIJ7Nu4c+vezbu378RKPMxuOOK38ePI
kytfjvvDcIUemEufTr26debPEYK4zr279+/gL2f/L/ghvPnz6NNXHy9wu/r38OPL
Zz0+xPz7+PPrfzzc/f7/AAYoX2DRCWjggQhyp4RzXo1QWoIQRiihb0CA0NUItk2o
4YYcqlbhVhh2KOKIJFoGBINXefBgiSy26KJhSmDl34s01jjiVTbmqOOGVe3o448I
TrXFkEQWaeSRSCap5JJMNunkk1BGKeWUVFZp5ZVYZqnlllx2meVRkYQp5phklmnm
mWimqeaabLbp5ptwxinnnHTWaeedeOap5558vtlTn4AGKuighBZq6KGIJqoonn8u
6uijkEYq6aSUVlpoo5ZmqummnHbq6adsYgrqqKSWauqpqLYpaqqsturqq7Be/8pT
rLTWauutuI65aq689urrr5HuCuywxBZr7JzCHqvssswWm2yz0EYrrate7OTFtNhm
qy2pXjCRExPXbivuuOQ+2q23NhEWbrnstuuunueiO1Nh675r7734phmvvC/NWG++
AAf87r78slQgvQInrDC5BC/YkoOH/bvwxBQrSzATH67EA2ISV+zxx7xezIQOK9Ww
IsIgp6yyrSIrMUJKJZyM8so014yqyEwsIZxJJCzWsc1AB20pzoRZSJIIjP0s9NJM
K0o0YSTZl3TTVFed6NNQi+SY0lZ37XWdWGf9UXGNcf312WivGbbYHJFddtpwx83m
2kwYvZHbb+M5xxp89//t99+ABy744IQXbvjhiCeu+OKMJ04HnXw0LvnklFdu+eWY
Aw7HnnQzsXNGPUNmtptoSGH66ainrvrqrLfu+uuwxy777LTXbvvsbdApx+289+77
78AHL7zqYHAu2csZSTZ6m6UP7/zz0EcvPeu5z7n79Nhnr/32rhcP72QkYISD8nk2
z/356KcvfPVyXq/++/DH373xksVokQ6TLc+m+fL377/67IuT+/5HwAJOz3t56lxh
blAR/OWvfAaMoASHF0A4DXCCGMyg7BCIJwUSZgkMlIgDH4gn/mnwhChMXQXfdMEU
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
3tOjAhkww2gXAfmNYjx02Lyc2L48RFWwBttNKG+wBlfKQ/adPR2wAVMHAR0wcRKm
3gIu01F0BWdwBkorKHGw4YJr2zqdQai7Avp9bgmwAiuguFxl4ZkNzVeUBWUw4zVt
J3ww42Xw1x5G2urTBC/w4yrNaD/+AphcX67NybCNQlrwX2BArHJSBkze2PXN4/FT
BDRw5bvrYxuA5WaJXS7uyCqqR1OQBWRe5mZ+5mfOTrftQkTQ5m7+5nAO585aSAAO
0xdO1JmFQQ2e5yb65ePrx3w+dlQe6H1+5Nddvwf/TehTzNWKzsx+rsIa3Og5zeiS
rsgUi8KN/OeRXunvs+ecDjt1LtR3vtefPum0XOqnvNFL3NFNvOmoTsyU/uqc++ht
DOiyjrunfusVrOpazOpcbOu6XrqdGuxpvMjhm+mQnt3EjuvMveyzbui+vsqJ7uy/
4+nOHupTPersTe2DnOvc/q28nsrRPs7T/u2GNOjfju1k3cnmTjvWvuzqrtfb3u7C
brn0/saOlLZ8+uKKfe8s6+3+nrPVPb+HXsDlHvCw8+7EHu/rbVUI/+/N/vCFPvAD
XPBlHQnK/fAKH+wMr+0OL/H5iu7c3vH8PuAg7zsbr+skD+amevK9k/K3vvKa/67s
Lu/uIk/tMp/sYV7zlXTz107rfezqPJ/wPg/vQO/ROz/0DbzmNZ/ztS70St86MC/r
Th/0NB/1pFT0C3/0rX71WE89Ws/xXP/rUP/1ssT0Ll/1SN/yZv86U//qat/1Sd/2
YI/2Jx/3ZD8ncVBjfN/3fv/3gB/4gj/4hF/4hn/4iJ/4ir/4id/hcKIHjB/5kj/5
lF/5ln/5f2+9FH/DFi83nv/5XqXvsVryoF/6QRNZ6276qn82qC/vq//6FNP6DQ/7
tC8wsu/xtZ/7+HL7pK/7vr/7ou+5vf/7xN8uvM/yxZ/8wI/ppIr8yv/8xh/8zjz8
0F/90HL8M2/92i8u2P+v89v//dPS/U8P/uQfLeJv9eWf/hYj/YhN/er//rFy/msP
//QfMuwf4O5f//pvKvIv9/v//wARSeBAggUNHkSYUOFCg16YPIQYUWLEHQAsXsSY
8SKOiR07emEYUuRIkiVNnkSZUuVKli1dvoQZU+bMlA493mRSUeNOjBxx3gRJU+hQ
okWNHkWaVOlSpjZ/TtTJk6fPpxODMsWaVetWrl29fnXptCrEqFI1Uh0L8SpYtm3d
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
DwgAOw==
"""


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

        # アイコン設定
        iconphoto = tk.PhotoImage(data=ICON)
        self.root.iconphoto(True, iconphoto)

        # ウィンドウ設定
        self.root.title(WINDOW_TITLE)                       # タイトル
        self.root.minsize(WINDOW_WIDTH-100, WINDOW_HEIGHT)  # 最小サイズ

        # メニューを配置
        self.menu = Menu(self, black_players, white_players)
        root.configure(menu=self.menu)

        # キャンバスを配置
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg=COLOR_BACKGROUND)
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
        if not cy.IMPORTED:
            self.canvas.coords(self.board.slowmode_text, SLOWMODE_OFFSET_X+dw, SLOWMODE_OFFSET_Y)

        # START
        self.canvas.coords(self.start.text, START_OFFSET_X+dwc+offset/2, START_OFFSET_Y+dhc+offset*2)

        # SQUARES
        square_w = self.board.square_w * area_ratio
        min_x, min_y = self.board.square_x_ini-offset, self.board.square_y_ini-offset
        max_x, max_y = min_x + square_w * self.size, min_y + square_w * self.size
        row_x, col_y = min_x - SQUAREHEADER_OFFSET_XY, min_y - SQUAREHEADER_OFFSET_XY
        # - board
        self.canvas.coords('board', min_x+dwc, min_y+dhc, max_x+dwc, max_y+dhc)
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
            fill=COLOR_CPUTIME_LABEL
        )

        # アシスト表示
        assist_text = 'Assist On' if self.assist == 'ON' else ''
        self.canvas.create_text(
            ASSIST_OFFSET_X,
            ASSIST_OFFSET_Y,
            text=assist_text,
            font=('', ASSIST_FONT_SIZE),
            anchor='w',
            fill=COLOR_ASSIST_LABEL
        )

        # 棋譜出力表示
        record_text = 'REC' if self.record == 'ON' else ''
        self.record_text = self.canvas.create_text(
            RECORD_OFFSET_X+dw,
            RECORD_OFFSET_Y,
            text=record_text,
            font=('', RECORD_FONT_SIZE),
            anchor='w',
            fill=COLOR_REC_LABEL
        )

        # 低速モードの表示
        slowmode_text = '■'
        if not cy.IMPORTED:
            self.slowmode_text = self.canvas.create_text(
                SLOWMODE_OFFSET_X+dw,
                SLOWMODE_OFFSET_Y,
                text=slowmode_text,
                font=('', SLOWMODE_FONT_SIZE),
                anchor='w',
                fill=COLOR_LOWSPEED_LABEL
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

        # 盤面の背景を描画
        self.canvas.create_rectangle(min_x+dwc, min_y+dhc, max_x+dwc, max_y+dhc, fill=COLOR_BOARD, outline=COLOR_BOARD, tag='board')

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
                    text = self.canvas.create_text(text_x+dwc, text_y+dhc, fill=COLOR_CELL_NUMBER, text=label, font=('', SQUAREHEADER_FONT_SIZE))
                    text_append(text)

                # マス目の線
                line = self.canvas.create_line(square_x1+dwc, square_y1+dhc, square_x2+dwc, square_y2+dhc, fill=COLOR_CELL_LINE)
                line_append(line)

            # 目印の描画
            if size > 4 and num == size//2 + 2:
                mark_w = int(w * OVAL_SIZE_RATIO * 0.2)
                for x_offset in [w * (num - 4), w * num]:
                    for y_offset in [w * (num - 4), w * num]:
                        mark_x1, mark_y1 = min_x + x_offset - mark_w//2, min_y + y_offset - mark_w//2
                        mark_x2, mark_y2 = min_x + x_offset + mark_w//2, min_y + y_offset + mark_w//2
                        oval = self.canvas.create_oval(mark_x1+dwc, mark_y1+dhc, mark_x2+dwc, mark_y2+dhc, tag='mark', fill=COLOR_CELL_MARK, outline=COLOR_CELL_MARK)  # noqa: E501
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
            disc_color = COLOR_PLAYER1_DISC if color == 'black' else COLOR_PLAYER2_DISC
            oval = self.canvas.create_oval(x1, y1, x2, y2, tag=label, fill=disc_color, outline=disc_color)
            self._discs[(label, color, index_x, index_y)] = oval

        # ひっくり返す途中
        else:
            w1, w2 = self.oval_w1 * self.area_ratio, self.oval_w2 * self.area_ratio
            label1 = self._get_label(color + '1', index_x, index_y)
            label2 = self._get_label(color + '2', index_x, index_y)
            color1 = COLOR_PLAYER2_DISC if color == 'turnblack' else COLOR_PLAYER1_DISC
            color2 = COLOR_PLAYER1_DISC if color == 'turnblack' else COLOR_PLAYER2_DISC

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
                self._squares[y][x] = self.canvas.create_rectangle(x1+dw, y1+dh, x2+dw, y2+dh, fill=COLOR_MOVE_HIGHLIGHT1, outline=COLOR_CELL_LINE, tag='moves')
            else:
                self._squares[y][x] = self.canvas.create_rectangle(x1+dw, y1+dh, x2+dw, y2+dh, fill=COLOR_BACKGROUND, outline=COLOR_CELL_LINE, tag='moves')
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
        self._squares[y][x] = self.canvas.create_rectangle(x1+dw, y1+dh, x2+dw, y2+dh, fill=COLOR_MOVE_HIGHLIGHT2, outline=COLOR_CELL_LINE, tag='move')
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
                self.canvas.itemconfigure(square, fill=COLOR_MOVE_HIGHLIGHT2)
        return _enter

    def _leave_selectable_moves(self, square):
        """打てる場所からカーソルが離れた
        """
        def _leave(event):
            if self.assist == 'ON':
                self.canvas.itemconfigure(square, fill=COLOR_MOVE_HIGHLIGHT1)
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
            fill=COLOR_START_MESSAGE1
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
        self.canvas.itemconfigure(self.text, fill=COLOR_START_MESSAGE2)

    def _leave_start(self, event):
        """カーソルが離れた時
        """
        self.canvas.itemconfigure(self.text, fill=COLOR_START_MESSAGE1)

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
