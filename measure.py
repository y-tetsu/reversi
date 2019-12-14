#!/usr/bin/env python
"""
計測
"""

import time


class Measure:
    """
    計測
    """
    elp_time = {}
    count = 0

    @classmethod
    def time(cls, key):
        """
        時間計測
        """
        Measure.elp_time[key] = {'min': 10000, 'max': 0, 'ave': 0, 'cnt': 0}

        def _time(func):
            def wrapper(*args, **kwargs):
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
        return _time

    @classmethod
    def countup(cls, func):
        """
        コール回数のカウントアップ
        """
        def _countup(*args, **kwargs):
            Measure.count += 1

            ret = func(*args, **kwargs)

            return ret
        return _countup
