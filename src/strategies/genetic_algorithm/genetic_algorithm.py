#!/usr/bin/env python
"""
遺伝的アルゴリズム
"""
import os
import json


# ToDo : Evaluator_TPWEのパラメータ調整
#        < corner=50, c=-20, a1=0, a2=-1, b=-1, x=-25, o=-5, wp=5, ww=10000, we=100 >
class GeneticAlgorithm:
    """
    遺伝的アルゴリズム
    """
    def __init__(self, initial_population, setting_json):
        self._population = initial_population
        self._setting = self._load_setting(setting_json)

    def _load_setting(self, setting_json):
        """
        設定ファイルのロード
        """
        setting = {
            "threshold": 0,
            "max_generations": 0,
            "mutation_chance": 0,
            "crossover_chance": 0,
            "selection_type": "ROULETTE"
        }

        if setting_json is not None and os.path.isfile(setting_json):
            with open(setting_json) as f:
                setting = json.load(f)

        return setting


if __name__ == '__main__':
    ga = GeneticAlgorithm([], './setting.json')
    print(ga._setting)
