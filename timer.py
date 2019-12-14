#!/usr/bin/env python
"""
タイマー
"""

import time


class TimerTimeoutError(Exception):
    pass


class Timer:
    """
    タイマー
    """
    deadline = {}

    @classmethod
    def start(cls, limit):
        """
        タイマー開始
        """
        def _start(func):
            def wrapper(*args, **kwargs):
                key = args[0].__class__.__name__
                Timer.deadline[key] = time.time() + limit  # デッドラインを設定する
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
                raise TimerTimeoutError("Timer Timeout Occuer!")

            return func(*args, **kwargs)
        return wrapper
