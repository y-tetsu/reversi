#!/usr/bin/env python
"""
GUIウィンドウ
"""

import tkinter as tk
from board import Board


WINDOW_WIDTH = 1360
WINDOW_HEIGHT = 680


class Window(tk.Frame):
    """
    ウィンドウ
    """
    def __init__(self, size=8, master=None):
        super().__init__(master)
        self.pack()

        self.canvas = tk.Canvas(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg='green')
        self.canvas.grid(row=0, column=1)

        self.black_name = self.canvas.create_text( 200, 80, text="●User1", tag="black_name", font=('', 32), fill='black')
        self.white_name = self.canvas.create_text(1150, 80, text="●User2", tag="white_name", font=('', 32), fill='white')

        self.black_num = self.canvas.create_text( 200, 250, text="676", tag="black_num", font=('', 140), fill='black')
        self.white_num = self.canvas.create_text(1150, 250, text="676", tag="white_num", font=('', 140), fill='white')

        self.black_result = self.canvas.create_text( 200, 400, text="勝ち", tag="black_result", font=('', 32), fill='black')
        self.white_result = self.canvas.create_text(1150, 400, text="反則", tag="white_result", font=('', 32), fill='white')

        self.black_turn = self.canvas.create_text( 200, 500, text="手番です", tag="black_turn", font=('', 32), fill='black')
        self.white_turn = self.canvas.create_text(1150, 500, text="手番です", tag="white_turn", font=('', 32), fill='white')

        self.black_move = self.canvas.create_text( 200, 600, text="(z, 26)に置きました", tag="black_move", font=('', 32), fill='black')
        self.white_move = self.canvas.create_text(1150, 600, text="(z, 26)に置きました", tag="white_move", font=('', 32), fill='white')

        self.start = self.canvas.create_text(680, 620, text="クリックでスタート", tag="start", font=('', 32), fill='yellow')

        self.size = size
        self.square_x_ini = 0
        self.square_y_ini = 0
        self.square_w = 0
        self.oval_w1 = 0
        self.oval_w2 = 0

        self.draw_squares(size)
        self.put_init_stone()

    def put_init_stone(self):
        """
        石を初期位置に置く
        """
        center = self.size // 2
        self.put_stone(Board.BLACK, center, center-1)
        self.put_stone(Board.BLACK, center-1, center)
        self.put_stone(Board.WHITE, center-1, center-1)
        self.put_stone(Board.WHITE, center, center)
        self.put_blackwhite(0, 0)
        self.put_whiteblack(0, 1)

    def put_stone(self, stone, index_x, index_y):
        """
        石を置く
        """
        if stone == Board.BLACK:
            self.put_black(index_x, index_y)
        else:
            self.put_white(index_x, index_y)

    def put_black(self, index_x, index_y):
        """
        黒を置く
        """
        x, y = self.get_coordinate(index_x, index_y)

        label_x = chr(x + 97)
        label_y = str(y + 1)

        black_id = self.canvas.create_oval( x - self.oval_w1/2, y - self.oval_w1/2, x + self.oval_w1/2, y + self.oval_w1/2, tag="black" + label_x + label_y, fill='black', outline='black')

    def put_white(self, index_x, index_y):
        """
        白を置く
        """
        x, y = self.get_coordinate(index_x, index_y)

        label_x = chr(x + 97)
        label_y = str(y + 1)

        white_id = self.canvas.create_oval( x - self.oval_w1/2, y - self.oval_w1/2, x + self.oval_w1/2, y + self.oval_w1/2, tag="white" + label_x + label_y, fill='white', outline='white')

    def put_blackwhite(self, index_x, index_y):
        """
        黒をひっくり返す途中
        """
        x, y = self.get_coordinate(index_x, index_y)

        label_x = chr(x + 97)
        label_y = str(y + 1)

        white_id = self.canvas.create_rectangle( x - self.oval_w2, y - self.oval_w1/2, x, y + self.oval_w1/2, tag="blackwhite1_" + label_x + label_y, fill='white', outline='white')
        black_id = self.canvas.create_rectangle( x, y - self.oval_w1/2, x + self.oval_w2, y + self.oval_w1/2, tag="blackwhite2_" + label_x + label_y, fill='black', outline='black')

    def put_whiteblack(self, index_x, index_y):
        """
        白をひっくり返す途中
        """
        x, y = self.get_coordinate(index_x, index_y)

        label_x = chr(x + 97)
        label_y = str(y + 1)

        black_id = self.canvas.create_rectangle( x - self.oval_w2, y - self.oval_w1/2, x, y + self.oval_w1/2, tag="whiteblack1_" + label_x + label_y, fill='black', outline='black')
        white_id = self.canvas.create_rectangle( x, y - self.oval_w1/2, x + self.oval_w2, y + self.oval_w1/2, tag="whitebalck2_" + label_x + label_y, fill='white', outline='white')

    def remove_stones(self):
        """
        すべての石を消す
        """
        for y in range(self.size):
            for x in range(self.size):
                self.remove_black(x, y)
                self.remove_white(x, y)
                self.remove_blackwhite(x, y)
                self.remove_whiteblack(x, y)

    def remove_black(self, index_x, index_y):
        """
        黒を消す
        """
        label_x = chr(index_x + 97)
        label_y = str(index_y + 1)

        self.remove_stone('black', label_x, label_y)


    def remove_white(self, index_x, index_y):
        """
        白を消す
        """
        label_x = chr(index_x + 97)
        label_y = str(index_y + 1)

        self.remove_stone('white', label_x, label_y)

    def remove_blackwhite(self, index_x, index_y):
        """
        黒白を消す
        """
        label_x = chr(index_x + 97)
        label_y = str(index_y + 1)

        self.remove_stone('blackwhite', label_x, label_y)

    def remove_whiteblack(self, index_x, index_y):
        """
        白黒を消す
        """
        label_x = chr(index_x + 97)
        label_y = str(index_y + 1)

        self.remove_stone('whiteblack', label_x, label_y)

    def remove_stone(self, stone, label_x, label_y):
        """
        石を消す
        """
        self.canvas.delete(stone + label_x + label_y)


    def get_coordinate(self, index_x, index_y):
        """
        座標を計算する
        """
        x_ini = self.square_x_ini
        y_ini = self.square_y_ini
        w = self.square_w

        return x_ini + w * index_x + w // 2, y_ini + w * index_y + w // 2

    def draw_squares(self, size):
        """
        オセロのマスを描く
        """
        self.size = size
        self.calc_size()

        y1 = self.square_y_ini

        for y in range(size):
            x1 = self.square_x_ini
            y2 = y1 + self.square_w
            for x in range(size):
                label_x = chr(x + 97)
                label_y = str(y + 1)
                x2 = x1 + self.square_w

                if not x:
                    self.canvas.create_text(x1-15, (y1+y2)//2, fill='white', text=label_y, tag='header_col', font=('', 20))

                if not y:
                    self.canvas.create_text((x1+x2)//2, y1-15, fill='white', text=label_x, tag='header_row', font=('', 20))

                self.canvas.create_rectangle(x1, y1, x2, y2, fill='green', outline='white', tag='square' + label_x + label_y)
                x1 = x2
            y1 = y2

    def calc_size(self):
        """
        サイズ計算
        """
        self.square_y_ini = 40
        self.square_w = (WINDOW_HEIGHT - self.square_y_ini - 120) // self.size
        self.square_x_ini = WINDOW_WIDTH // 2 - (self.square_w * self.size) // 2

        self.oval_w1 = int(self.square_w * 0.8)
        self.oval_w2 = int(self.square_w // 10)

    def remove_squares(self):
        """
        オセロのマスを消す
        """
        self.canvas.delete('header_col')
        self.canvas.delete('header_row')

        for y in range(self.size):
            for x in range(self.size):
                #label_x = chr(x + 97)
                #label_y = str(y + 1)
                label_x, label_y = self.get_label_index(x, y)
                self.canvas.delete('square' + label_x + label_y)

    def get_label_index(self, x, y):
        """
        表示ラベルのインデックスを返す
        """
        return chr(x + 97), str(y + 1)


class Menu(tk.Menu):
    """
    メニュー
    """
    def __init__(self, master=None):
        super().__init__(master)
        self.create_size_menu()
        self.create_black_menu()
        self.create_white_menu()
        self.master = master

    def create_size_menu(self):
        """
        ボードのサイズ
        """
        menu_size = tk.Menu(self)
        for i in range(4, 27, 2):
            menu_size.add_command(label=str(i), command=change_board_size(i, self.master))
        self.add_cascade(menu=menu_size, label='Size')

    def create_black_menu(self):
        """
        黒プレイヤー
        """
        menu_black = tk.Menu(self)
        for player in ['User1', 'Random', 'Greedy', 'Unselfish']:
            menu_black.add_command(label=player, command=change_black_player(player, self.master))
        self.add_cascade(menu=menu_black, label='Black')

    def create_white_menu(self):
        """
        白プレイヤー
        """
        menu_white = tk.Menu(self)
        for player in ['User1', 'Random', 'Greedy', 'Unselfish']:
            menu_white.add_command(label=player, command=change_white_player(player, self.master))
        self.add_cascade(menu=menu_white, label='White')


def change_black_player(player, master):
    """
    黒プレーヤーを変更
    """
    def change_player():
        master.canvas.delete('black_name')
        master.black_name = master.canvas.create_text( 200, 80, text="●" + player, tag="black_name", font=('', 32), fill='black')
    return change_player

def change_white_player(player, master):
    """
    白プレーヤーを変更
    """
    def change_player():
        master.canvas.delete('white_name')
        master.white_name = master.canvas.create_text(1150, 80, text="●" + player, tag="white_name", font=('', 32), fill='white')
    return change_player

def change_board_size(size, master):
    """
    ボードサイズの変更
    """
    def redraw_board_square():
        print(str(size))
        master.remove_stones()
        master.remove_squares()
        print(str(master.oval_w1))
        print(str(master.oval_w2))

        master.draw_squares(size)
        master.put_init_stone()

    return redraw_board_square


if __name__ == '__main__':
    window = Window(4)
    window.master.title('othello')                      # タイトル
    window.master.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)  # 最小サイズ
    window.master['menu'] = Menu(window)                # メニューをセット
    window.master.mainloop()
