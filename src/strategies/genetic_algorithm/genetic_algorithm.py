#!/usr/bin/env python
"""
遺伝的アルゴリズム
"""
import sys
import os
import json
from random import choices, random
from heapq import nlargest
from statistics import mean


class GeneticAlgorithm:
    """
    遺伝的アルゴリズム
    """
    def __init__(self, generation, setting_json, chromosome_cls):
        self._generation = generation
        self._setting = self._load_setting(setting_json)
        self._population = [chromosome_cls.random_instance() for _ in range(self._setting["population_num"])]
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
            "large_mutation": 0,
            "crossover_chance": 0
        }

        if setting_json is not None and os.path.isfile(setting_json):
            with open(setting_json) as f:
                setting = json.load(f)

        return setting

    def _generation_change(self):
        """
        世代交代(MGG-best2)
        """
        new_population = []

        # 個体群の中から親を2つランダムに選ぶ
        parent1, parent2 = random.sample(self._population, 2)
        self._population.remove(parent1)
        self._population.remove(parent2)

        # 選ばれた親個体間で交叉を行い、子個体を offspring_num 個生成する
        # 親個体と子個体全ての適応度を求める
        # 最良の適応度の個体を2つ選ぶ
        # 2つの個体を親個体と入れ替える
        #while len(new_population) < len(self._population):
        #    # 両親を選ぶ
        #    if self._setting["selection_type"] == "ROULETTE":
        #        parents = self._pick_roulette([x.fitness() + 0.001 for x in self._population])
        #    else:
        #        parents = self._pick_tournament(len(self._population) // 2)

        #    # 両親の交差
        #    if random() < self._setting["crossover_chance"]:
        #        print(' + crossover')
        #        new_population.extend(parents[0].crossover(parents[1]))
        #    else:
        #        for parent in parents:
        #            # 同じ個体は増やさない
        #            for individual in new_population:
        #                if parent == individual:
        #                    print('skip')
        #                    break
        #            else:
        #                new_population.append(parent)

        ## 個数合わせ
        #if len(new_population) > len(self._population):
        #    for _ in range(len(new_population) - len(self._population)):
        #        new_population.pop()

        #self._population = new_population

    def _mutate(self):
        """
        変異
        """
        for individual in self._population:
            if (self._generation + 1) % self._setting["large_mutation"] == 0:
                print(' + large_mutate')
                individual.large_mutate()
            else:
                if random() < self._setting["mutation_chance"]:
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
            print()
            print('best')
            print(best)
            print()

            if best.is_optimal():
                return best

            #---
            type(self._population[0]).save_population(self, './population' + str(self._generation) + '.json')
            #---

            print(f"\n*****\nGeneration {self._generation} Best {best.fitness()} Avg {mean(map(self._fitness_key, self._population))}\n*****\n")

            self._generation_change()
            self._generation += 1
            self._mutate()
            self._reset_fitness()

            highest = max(self._population, key=self._fitness_key)

            if highest.fitness() > best.fitness():
                best = highest

        print()
        print('best')
        print(best)
        print()
        print(f"\n*****\nGeneration {self._generation} Best {best.fitness()} Avg {mean(map(self._fitness_key, self._population))}\n*****\n")

        self.best = best

        return best

if __name__ == '__main__':
    from random import randrange
    from chromosome import Chromosome

    class Test(Chromosome):
        def __init__(self, parameter):
            self.parameter = parameter

        def fitness(self):
            pass

        def reset_fitness(self):
            pass

        def is_optimal(self):
            pass

        @classmethod
        def random_instance(cls):
            return Test(randrange(100))

        def fitness(self):
            pass

        def crossover(self):
            pass

        def mutate(self):
            pass

        def large_mutate(self):
            pass

    ga = GeneticAlgorithm(0, './ga_setting.json', Test)

    for individual in ga._population:
        print(individual.parameter)



