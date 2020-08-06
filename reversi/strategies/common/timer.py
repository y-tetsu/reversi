"""Timer
"""

import time
import os

from reversi.strategies.common import CPU_TIME


class Timer:
    """
    タイマー
    """
    deadline = {}
    timeout_flag = {}
    timeout_value = {}
    time_limit = CPU_TIME

    @classmethod
    def get_pid(cls, obj):
        """
        プロセスID取得
        """
        return obj.__class__.__name__ + str(os.getpid())

    @classmethod
    def set_deadline(cls, pid, value):
        """
        期限を設定
        """
        Timer.deadline[pid] = time.time() + Timer.time_limit  # デッドラインを設定する
        Timer.timeout_flag[pid] = False                       # タイムアウト未発生
        Timer.timeout_value[pid] = value                      # タイムアウト発生時の値を設定する

    @classmethod
    def start(cls, value):
        """
        タイマー開始
        """
        def _start(func):
            def wrapper(*args, **kwargs):
                pid = cls.get_pid(args[0])
                cls.set_deadline(pid, value)
                return func(*args, **kwargs)
            return wrapper
        return _start

    @classmethod
    def timeout(cls, func):
        """
        タイマー経過チェック
        """
        def wrapper(*args, **kwargs):
            pid = cls.get_pid(args[0])
            if time.time() > Timer.deadline[pid]:
                Timer.timeout_flag[pid] = True  # タイムアウト発生
                return Timer.timeout_value[pid]
            return func(*args, **kwargs)
        return wrapper

    @classmethod
    def is_timeout(cls, pid):
        """
        タイムアウト発生有無
        """
        if pid in Timer.timeout_flag:
            return Timer.timeout_flag[pid]

        return False
