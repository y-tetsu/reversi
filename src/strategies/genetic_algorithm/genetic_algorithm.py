#!/usr/bin/env python
"""
遺伝的アルゴリズム
"""
import os
import json
import random
from heapq import nlargest
from statistics import mean


class GeneticAlgorithm:
    """
    遺伝的アルゴリズム
    """
    def __init__(self, setting_json, chromosome_cls):
        self._setting = self._load_setting(setting_json)

        self._generation = 0
        self._population = [chromosome_cls.random_instance() for _ in range(self._setting["population_num"])]

        if os.path.isfile('./population.json'):
            if hasattr(type(self._population[0]), 'load_population'):
                self.generation, self.population = chromosome_cls.load_population('./population.json')
        else:
            print('[random_instance]')

        self._fitness_key = type(self._population[0]).fitness
        self.best = None

    def _load_setting(self, setting_json):
        """
        設定ファイルのロード
        """
        setting = {
            "population_num": 0,
            "offspring_num": 0,
            "max_generations": 0,
            "mutation_chance": 0,
            "large_mutation": 0
        }

        if setting_json is not None and os.path.isfile(setting_json):
            with open(setting_json) as f:
                setting = json.load(f)

        return setting

    def _generation_change(self):
        """
        世代交代(MGG-best2)
        """
        # 個体群の中から親を2つランダムに選ぶ
        parent1, parent2 = random.sample(self._population, 2)
        self._population.remove(parent1)
        self._population.remove(parent2)

        # 選ばれた親個体間で交叉を行い、子個体を offspring_num 個生成する
        offspring_num = self._setting["offspring_num"]
        offsprings = []

        while len(offsprings) < offspring_num:
            offsprings.append(parent1.crossover(parent2))

        # 親個体と子個体全ての適応度を求め最良の適応度の個体を2つ選び入れ替える
        offsprings.extend((parent1, parent2))
        best1, best2 = nlargest(2, offsprings, key=self._fitness_key)
        self._population.extend((best1, best2))

    def _mutate(self):
        """
        変異
        """
        for individual in self._population:
            if self._generation and self._generation % self._setting["large_mutation"] == 0:
                print(' + large_mutate')
                individual.large_mutate()
            else:
                if random.random() < self._setting["mutation_chance"]:
                    print(' + mutate')
                    individual.mutate()

    def _reset_fitness(self):
        """
        個体の適応度をリセット
        """
        for individual in self._population:
            individual.reset_fitness()

    def run(self):
        """
        実行
        """
        best = max(self._population, key=self._fitness_key)

        for generation in range(self._setting["max_generations"]):
            print(f"Generation {self._generation} Best {best.fitness()} Avg {mean(map(self._fitness_key, self._population))}")
            print('best:', best)
            print()

            if best.is_optimal():
                print('----- optimal pattern is found! -----')
                if hasattr(type(self._population[0]), 'save_population'):
                    type(self._population[0]).save_population(self, './population.json')
                self.best = best
                return best
            else:
                if hasattr(type(self._population[0]), 'save_population'):
                    type(self._population[0]).save_population(self, './population' + str(self._generation) + '.json')

            self._generation_change()
            self._generation += 1
            self._mutate()
            self._reset_fitness()

            highest = max(self._population, key=self._fitness_key)

            if highest.fitness() > best.fitness():
                best = highest

        print(f"Generation {self._generation} Best {best.fitness()} Avg {mean(map(self._fitness_key, self._population))}")

        if hasattr(type(self._population[0]), 'save_population'):
            type(self._population[0]).save_population(self, './population.json')

        self.best = best

        return best

if __name__ == '__main__':
    from random import randrange
    from copy import deepcopy

    from chromosome import Chromosome

    class Test(Chromosome):
        """
        乱数を足しながら77にする
        """
        def __init__(self, parameter):
            self.parameter = parameter
            self.name = str(parameter)

        def fitness(self):
            return 100 - abs(77 - self.parameter)

        def reset_fitness(self):
            pass

        def is_optimal(self):
            return self.parameter == 77

        @classmethod
        def random_instance(cls):
            return Test(randrange(100))

        def crossover(self, other):
            child = deepcopy(self)

            parent1 = 0 if self.parameter == 0 else randrange(self.parameter)
            parent2 = 0 if other.parameter == 0 else randrange(other.parameter)

            child.parameter = (parent1 + parent2) % 100
            child.name = '(' + self.name + '&' + other.name + ')'

            return child

        def mutate(self):
            self.parameter = (self.parameter + 1) % 100

        def large_mutate(self):
            self.parameter = randrange(100)
            self.name = str(self.parameter)

        def __str__(self):
            return 'name=' + self.name + " parameter=" + str(self.parameter)

    ga = GeneticAlgorithm('./ga_setting.json', Test)
    result = ga.run()
    print('result:', result)
