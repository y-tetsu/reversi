#!/usr/bin/env python
"""
遺伝的アルゴリズム
"""
import os
import json
from random import choices, random
from heapq import nlargest
from chromosome import Chromosome


# ToDo : Evaluator_TPWEのパラメータ調整
#        < corner=50, c=-20, a1=0, a2=-1, b=-1, x=-25, o=-5, wp=5, ww=10000, we=100 >
class GeneticAlgorithm:
    """
    遺伝的アルゴリズム
    """
    def __init__(self, initial_population, setting_json):
        self._population = initial_population
        self._setting = self._load_setting(setting_json)
        self._fitness_key = type(self._population[0]).fitness

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

    def _pick_roulette(self, wheel):
        """
        ルーレット選択
        """
        return tuple(choices(self._population, weight=wheel, k=2))

    def _pick_tournament(self, num_participants):
        """
        トーナメント選択
        """
        participants = choices(self._population, k=num_participants)

        return tuple(nlargest(2, participants, key=self._fitness_key))


if __name__ == '__main__':
    pass
    #ga = GeneticAlgorithm([], './setting.json')
    #print(ga._setting)
