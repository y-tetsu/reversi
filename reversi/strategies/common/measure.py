#!/usr/bin/env python
"""
計測
"""

import time
import os


class Measure:
    """
    計測
    """
    elp_time = {}
    count = {}

    @classmethod
    def time(cls, func):
        """
        時間計測
        """
        def wrapper(*args, **kwargs):
            key = args[0].__class__.__name__ + str(os.getpid())

            if key not in Measure.elp_time:
                Measure.elp_time[key] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}

            time_s = time.perf_counter()
            ret = func(*args, **kwargs)
            time_e = time.perf_counter()
            elp = time_e - time_s

            if elp > Measure.elp_time[key]['max']:
                Measure.elp_time[key]['max'] = elp
            if elp < Measure.elp_time[key]['min']:
                Measure.elp_time[key]['min'] = elp

            pre_cnt = Measure.elp_time[key]['cnt']
            pre_ave = Measure.elp_time[key]['ave']

            Measure.elp_time[key]['ave'] = ((pre_ave * pre_cnt) + elp) / (pre_cnt + 1)
            Measure.elp_time[key]['cnt'] += 1

            return ret
        return wrapper

    @classmethod
    def countup(cls, func):
        """
        コール回数のカウントアップ
        """
        def wrapper(*args, **kwargs):
            if 'pid' in kwargs:
                pid = kwargs['pid']
                if pid not in Measure.count:
                    Measure.count[pid] = 0
                Measure.count[pid] += 1

            return func(*args, **kwargs)
        return wrapper
