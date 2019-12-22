#!/usr/bin/env python
"""
タイマー
"""

import time


class Timer:
    """
    タイマー
    """
    deadline = {}
    timeout_flag = {}

    @classmethod
    def start(cls, limit):
        """
        タイマー開始
        """
        def _start(func):
            def wrapper(*args, **kwargs):
                key = args[0].__class__.__name__

                Timer.deadline[key] = time.time() + limit  # デッドラインを設定する
                Timer.timeout_flag[key] = False            # タイムアウト未発生

                ret = func(*args, **kwargs)

                return ret
            return wrapper
        return _start

    @classmethod
    def timeout(cls, func):
        """
        タイマー経過チェック
        """
        def wrapper(*args, **kwargs):
            key = args[0].__class__.__name__

            if time.time() > Timer.deadline[key]:
                Timer.timeout_flag[key] = True  # タイムアウト発生

                return 0

            return func(*args, **kwargs)
        return wrapper

    @classmethod
    def is_timeout(cls, obj):
        """
        タイムアウト発生有無
        """
        return Timer.timeout_flag[obj.__class__.__name__]
