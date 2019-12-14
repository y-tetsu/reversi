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
            return func(*args, **kwargs) if time.time() < Timer.deadline[key] else 0

        return wrapper
