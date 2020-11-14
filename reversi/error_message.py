"""ErrorMessage
"""

import tkinter as tk


class ErrorMessage:
    """
    エラーメッセージ
    """
    def __init__(self):
        self.root = None
        self.label = None
        self.title = 'Error'
        self.minx = 300
        self.miny = 30
        self.fill = 'x'
        self.padx = '5'
        self.pady = '5'

    def show(self, message):
        """
        エラーメッセージを表示
        """
        self.root = tk.Tk()
        self.root.title(self.title)
        self.root.minsize(self.minx, self.miny)
        self.label = tk.Label(self.root, text=message)
        self.label.pack(fill=self.fill, padx=self.padx, pady=self.pady)
        self._start_window()

    def _start_window(self):
        """
        ウィンドウ起動
        """
        self.root.mainloop()
