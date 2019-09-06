#!/usr/bin/env python
"""
GUIウィンドウ
"""

import tkinter as tk
import board
from board import Board


WINDOW_WIDTH = 1360
WINDOW_HEIGHT = 680



class Window(tk.Frame):
    """
    ウィンドウ
    """
    def __init__(self, size=8, master=None, event=None, queue=None):
        super().__init__(master)
        self.pack()

        self.event = event
        self.queue = queue

        self.canvas = tk.Canvas(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg='green')
        self.canvas.grid(row=0, column=1)

        self.black_name = self.canvas.create_text( 200, 80, text="●User1", tag="black_name", font=('', 32), fill='black')
        self.white_name = self.canvas.create_text(1150, 80, text="●User2", tag="white_name", font=('', 32), fill='white')
        self.black_num = self.canvas.create_text( 200, 250, text="2", tag="black_num", font=('', 140), fill='black')
        self.white_num = self.canvas.create_text(1150, 250, text="2", tag="white_num", font=('', 140), fill='white')
        self.black_result = self.canvas.create_text( 200, 400, text="", tag="black_result", font=('', 32), fill='black')
        self.white_result = self.canvas.create_text(1150, 400, text="", tag="white_result", font=('', 32), fill='white')
        self.black_turn = self.canvas.create_text( 200, 500, text="", tag="black_turn", font=('', 32), fill='orange')
        self.white_turn = self.canvas.create_text(1150, 500, text="", tag="white_turn", font=('', 32), fill='orange')
        self.black_move = self.canvas.create_text( 200, 600, text="", tag="black_move", font=('', 32), fill='black')
        self.white_move = self.canvas.create_text(1150, 600, text="", tag="white_move", font=('', 32), fill='white')

        self.start = self.canvas.create_text(680, 620, text="クリックでスタート", tag="start", font=('', 32), fill='yellow')

        self.size = size
        self.square_x_ini = 0
        self.square_y_ini = 0
        self.square_w = 0
        self.oval_w1 = 0
        self.oval_w2 = 0

        self.calc_size()
        self.draw_squares()
        self.put_init_stones()

        self.menubar = Menu(self, self.event, self.queue)  # メニューをセット
        master.configure(menu=self.menubar)

    def calc_size(self):
        """
        サイズ計算
        """
        self.square_y_ini = 40
        self.square_w = (WINDOW_HEIGHT - self.square_y_ini - 120) // self.size
        self.square_x_ini = WINDOW_WIDTH // 2 - (self.square_w * self.size) // 2

        self.oval_w1 = int(self.square_w * 0.8)
        self.oval_w2 = int(self.square_w // 10)

    def put_init_stones(self):
        """
        石を初期位置に置く
        """
        center = self.size // 2
        self.put_stone(Board.BLACK, center, center-1)
        self.put_stone(Board.BLACK, center-1, center)
        self.put_stone(Board.WHITE, center-1, center-1)
        self.put_stone(Board.WHITE, center, center)

    def update_board(self, board):
        """
        ボードの状態を反映する
        """
        pass

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
        label = self.get_label("black", index_x, index_y)

        x, y = self.get_coordinate(index_x, index_y)

        x1 = x - self.oval_w1/2
        y1 = y - self.oval_w1/2
        x2 = x + self.oval_w1/2
        y2 = y + self.oval_w1/2

        black_id = self.canvas.create_oval(x1, y1, x2, y2, tag=label, fill='black', outline='black')

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

        white_id = self.canvas.create_oval(x1, y1, x2, y2, tag=label, fill='white', outline='white')

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

        white_id = self.canvas.create_rectangle(x1, y1, x2, y2, tag=label1, fill='white', outline='white')

        x1 = x
        x2 = x + self.oval_w2
        black_id = self.canvas.create_rectangle(x1, y1, x2, y2, tag=label2, fill='black', outline='black')

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

        black_id = self.canvas.create_rectangle(x1, y1, x2, y2, tag=label1, fill='black', outline='black')

        x1 = x
        x2 = x + self.oval_w2
        white_id = self.canvas.create_rectangle(x1, y1, x2, y2, tag=label2, fill='white', outline='white')

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

    def draw_squares(self):
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
                    self.canvas.create_text(x1-15, (y1+y2)//2, fill='white', text=label_y, tag='header_col', font=('', 20))

                if not y:
                    self.canvas.create_text((x1+x2)//2, y1-15, fill='white', text=label_x, tag='header_row', font=('', 20))

                self.canvas.create_rectangle(x1, y1, x2, y2, fill='green', outline='white', tag='square_' + label_x + label_y)

                x1 = x2
            y1 = y2

    def remove_squares(self):
        """
        オセロのマスを消す
        """
        self.canvas.delete('header_col')
        self.canvas.delete('header_row')

        for y in range(self.size):
            for x in range(self.size):
                label = self.get_label('square', x, y)
                print(label)
                self.canvas.delete(label)

    def get_label(self, name, x, y):
        """
        表示ラベルを返す
        """
        return name + "_" + chr(x + 97) + str(y + 1)


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
        self.add_cascade(menu=menu_size, label='Size')

    def create_black_menu(self):
        """
        黒プレイヤー
        """
        menu_black = tk.Menu(self)
        for player in ['User1', 'Random', 'Greedy', 'Unselfish']:
            menu_black.add_command(label=player, command=self.change_black_player(player, self.master))
        self.add_cascade(menu=menu_black, label='Black')

    def create_white_menu(self):
        """
        白プレイヤー
        """
        menu_white = tk.Menu(self)
        for player in ['User2', 'Random', 'Greedy', 'Unselfish']:
            menu_white.add_command(label=player, command=self.change_white_player(player, self.master))
        self.add_cascade(menu=menu_white, label='White')

    def change_board_size(self, size):
        """
        ボードサイズの変更
        """
        def change_board_size_event():
            self.entryconfigure('Size', state='disable')

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

        return change_player

    def change_white_player(self, player, master):
        """
        白プレーヤーを変更
        """
        def change_player():
            master.canvas.itemconfigure(master.white_name, text="●" + player)

        return change_player


if __name__ == '__main__':
    import time
    import threading
    import queue

    event = threading.Event()
    q = queue.Queue()

    def demo(window):
        global event, q

        print("board size", window.size)

        while True:
            if event.is_set():
                window.remove_stones()
                window.remove_squares()

                window.size = q.get()
                print("board size changed", window.size)
                window.calc_size()
                window.draw_squares()
                window.put_init_stones()
                event.clear()

                window.menubar.entryconfigure('Size', state='normal')

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

    app = tk.Tk()
    app.withdraw()  # 表示が整うまで隠す

    window = Window(master=app, event=event, queue=q)
    window.master.title('othello')                      # タイトル
    window.master.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)  # 最小サイズ

    game = threading.Thread(target=demo, args=([window]))
    game.daemon = True
    game.start()

    app.deiconify()  # 表示する
    app.mainloop()
