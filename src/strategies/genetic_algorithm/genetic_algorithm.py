#!/usr/bin/env python
"""
遺伝的アルゴリズム
"""
import os
import json
from random import choices, random
from heapq import nlargest
from statistics import mean

from chromosome import Chromosome


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

    def _generation_change(self):
        """
        世代交代
        """
        new_population = []

        while len(new_population) < len(self._population):
            # 両親を選ぶ
            if self._setting["selection_type"] == "ROULETTE":
                parents = self._pick_roulette([x.fitness() for x in self._population])
            else:
                parents = self._pick_tournament(len(self._population) // 2)

            # 両親の交差
            if random() < self._setting["crossover_chance"]:
                new_population.extend(parents[0].crossover(parents[1]))
            else:
                new_population.extend(parents)

        # 個数合わせ
        if len(new_population) > len(self._population):
            for _ in range(len(new_population) - len(self._population)):
                new_population.pop()

        self._population = new_population

    def _mutate(self):
        """
        変異
        """
        for individual in self._population:
            if random() < self._setting["mutation_chance"]:
                individual.mutate()

    def run(self):
        """
        実行
        """
        best = max(self._population, key=self._fitness_key)

        for generation in range(self._setting["max_generations"]):
            if best.fitness() >= self._setting["threshold"]:
                return best

            print(f"Generation {generation} Best {best.fitness()} Avg {mean(map(self._fitness_key, self._population))}")

            self._generation_change()
            self._mutate()

            highest = max(self._population, key=self._fitness_key)

            if highest.fitness() > best.fitness():
                best = highest

        return best


if __name__ == '__main__':
    # ToDo : Evaluator_TPWEのパラメータ調整
    #        < corner=50, c=-20, a1=0, a2=-1, b=-1, x=-25, o=-5, wp=5, ww=10000, we=100 >

    #ga = GeneticAlgorithm([], './setting.json')
    #print(ga._setting)
    pass
