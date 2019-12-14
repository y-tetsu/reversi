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
    limit = {}

    @classmethod
    def start(cls, key, limit):
        """
        タイマー開始
        """
        Timer.limit[key] = limit

        def _set_timer(func):
            def wrapper(*args, **kwargs):
                Timer.deadline[key] = time.time() + limit

                ret = func(*args, **kwargs)

                return ret
            return wrapper
        return _set_timer

    @classmethod
    def timeout(cls, key):
        """
        タイマー経過チェック
        """
        def _timeout(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs) if time.time() < Timer.deadline[key] else 0

            return wrapper
        return _timeout
