#!/usr/bin/env python
"""
タイマー
"""

import time
import os


class Timer:
    """
    タイマー
    """
    deadline = {}
    timeout_flag = {}
    timeout_value = {}

    @classmethod
    def set_deadline(cls, name, limit, value):
        """
        期限を設定
        """
        key = name + str(os.getpid())
        Timer.deadline[key] = time.time() + limit  # デッドラインを設定する
        Timer.timeout_flag[key] = False            # タイムアウト未発生
        Timer.timeout_value[key] = value           # タイムアウト発生時の値を設定する

    @classmethod
    def start(cls, limit, value):
        """
        タイマー開始
        """
        def _start(func):
            def wrapper(*args, **kwargs):
                name = args[0].__class__.__name__
                cls.set_deadline(name, limit, value)
                return func(*args, **kwargs)
            return wrapper
        return _start

    @classmethod
    def timeout(cls, func):
        """
        タイマー経過チェック
        """
        def wrapper(*args, **kwargs):
            key = args[0].__class__.__name__ + str(os.getpid())
            if time.time() > Timer.deadline[key]:
                Timer.timeout_flag[key] = True  # タイムアウト発生
                return Timer.timeout_value[key]
            return func(*args, **kwargs)
        return wrapper

    @classmethod
    def is_timeout(cls, obj):
        """
        タイムアウト発生有無
        """
        return Timer.timeout_flag[obj.__class__.__name__ + str(os.getpid())]
