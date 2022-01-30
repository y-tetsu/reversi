#!/usr/bin/env python
"""
Switch2_TWのパラメータ調整
"""

if '__file__' in globals():
    import os, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


import json
from random import randrange, random, randint
from copy import deepcopy

from reversi import Player, Simulator
from reversi.strategies.joseki import Ushi, Hitsuji
from reversi.strategies.fullreading import FullReading
from reversi.strategies.switch import Switch
from reversi.strategies.minmax import MinMax
from reversi.strategies.table import Table
from reversi.strategies.coordinator import Evaluator_TW
from reversi.genetic_algorithm.chromosome import Chromosome
from reversi.genetic_algorithm.genetic_algorithm import GeneticAlgorithm


MAX_WEIGHT = 250


class Switch2_TW(Chromosome):
    """
    Switch2_TWのパラメータ調整
    """
    def __init__(self, corner=None, c=None, a1=None, a2=None, b=None, o=None, x=None, ww=None):
        self.setting = self._load_setting('./ga_setting.json')
        self.param = [corner, c, a1, a2, b, o, x, ww]
        self.fitness_value = None

    def _load_setting(self, setting_json):
        """
        設定値読み込み
        """
        setting = {}
        if setting_json is not None and os.path.isfile(setting_json):
            with open(setting_json) as f:
                setting = json.load(f)

        return setting

    def fitness(self):
        """
        適応度
        """
        if self.fitness_value is not None:
            return self.fitness_value

        simulator = Simulator(
            {
                # 遺伝個体(MinMax2_TW-Switch)
                'Challenger': Hitsuji(
                    base=FullReading(
                        remain=9,
                        base=Switch(
                            turns=self.setting['turns'],
                            strategies=[
                                MinMax(
                                    depth=2,
                                    evaluator=Evaluator_TW(
                                        corner=self.param[0][i],
                                        c=self.param[1][i],
                                        a1=self.param[2][i],
                                        a2=self.param[3][i],
                                        b=self.param[4][i],
                                        o=self.param[5][i],
                                        x=self.param[6][i],
                                        ww=self.param[7][i],
                                    ),
                                ) for i in range(len(self.setting['turns']))
                            ],
                        ),
                    ),
                ),
                # 対戦相手(MinMax2_TW)
                'Opponent': Ushi(
                    base=FullReading(
                        remain=9,
                        base=MinMax(
                                depth=2,
                                evaluator=Evaluator_TW(),
                        ),
                    ),
                ),
            },
            './ga_setting.json',
        )

        simulator.start()
        print(simulator)
        self.fitness_value = ((simulator.result_ratio['Challenger'] - simulator.result_ratio['Opponent']) + 100) / 2

        return self.fitness_value

    def reset_fitness(self):
        """
        適応度のリセット
        """
        self.fitness_value = None

    def is_optimal(self):
        """
        最適解が見つかったか判定
        """
        return self.fitness() >= self.setting['threshold']

    @classmethod
    def random_instance(cls):
        """
        初期パラメータ設定
        """
        switch_num = len(Switch2_TW().setting['turns'])
        corner = [randrange(MAX_WEIGHT) * (1 if random() > 0.5 else -1) for _ in range(switch_num)]
        c = [randrange(MAX_WEIGHT) * (1 if random() > 0.5 else -1) for _ in range(switch_num)]
        a1 = [randrange(MAX_WEIGHT) * (1 if random() > 0.5 else -1) for _ in range(switch_num)]
        a2 = [randrange(MAX_WEIGHT) * (1 if random() > 0.5 else -1) for _ in range(switch_num)]
        b = [randrange(MAX_WEIGHT) * (1 if random() > 0.5 else -1) for _ in range(switch_num)]
        x = [randrange(MAX_WEIGHT) * (1 if random() > 0.5 else -1) for _ in range(switch_num)]
        o = [randrange(MAX_WEIGHT) * (1 if random() > 0.5 else -1) for _ in range(switch_num)]
        ww = [100000 for _ in range(switch_num)]

        return Switch2_TW(corner=corner, c=c, a1=a1, a2=a2, b=b, o=o, x=x, ww=ww)

    def crossover(self, other):
        """
        交叉
        """
        child = deepcopy(self) if random() > 0.5 else deepcopy(other)
        child.reset_fitness()

        p_low, p_high = randrange(len(self.param)), randrange(len(self.param))
        (p_low, p_high) = (p_low, p_high) if p_low < p_high else (p_high, p_low)
        switch_num = len(self.param[0])
        for param_index in range(p_low, p_high+1):
            s_low, s_high = randrange(switch_num), randrange(switch_num)
            (s_low, s_high) = (s_low, s_high) if s_low < s_high else (s_high, s_low)
            for stage_index in range(s_low, s_high+1):
                v_low, v_high = self.param[param_index][stage_index], other.param[param_index][stage_index]
                (v_low, v_high) = (v_low, v_high) if v_low < v_high else (v_high, v_low)
                child.param[param_index][stage_index] = randint(v_low, v_high)

        return child

    def mutate(self):
        """
        変異(摂動)
        """
        param_index = randrange(len(self.param))
        stage_index = randrange(len(self.setting['turns']))
        self.param[param_index][stage_index] += self.setting['mutation_value'] * (1 if random() > 0.5 else -1)

    def large_mutate(self):
        """
        大変異(摂動)
        """
        param_index = randrange(len(self.param))
        stage_index = randrange(len(self.setting['turns']))
        self.param[param_index][stage_index] += self.setting['large_mutation_value'] * (1 if random() > 0.5 else -1)

    def __str__(self):
        return f"corner: {self.param[0]}\nc: {self.param[1]}\na1: {self.param[2]}\na2: {self.param[3]}\nb: {self.param[4]}\no: {self.param[5]}\nx: {self.param[6]}\nww: {self.param[7]}\nFitness: {self.fitness()}"

    @classmethod
    def load_population(cls, json_file):
        """
        母集団の取得
        """
        generation, population = 0, {}
        if json_file is not None and os.path.isfile(json_file):
            with open(json_file) as f:
                json_setting = json.load(f)

                generation = json_setting["generation"]
                corner = json_setting['corner']
                c = json_setting['c']
                a1 = json_setting['a1']
                a2 = json_setting['a2']
                b = json_setting['b']
                o = json_setting['o']
                x = json_setting['x']
                ww = json_setting['ww']

                population = [Switch2_TW(corner=corner[i], c=c[i], a1=a1[i], a2=a2[i], b=b[i], o=o[i], x=x[i], ww=ww[i]) for i in range(len(corner))]

        return generation, population

    @classmethod
    def save_population(cls, ga, json_file):
        """
        母集団の保存
        """
        generation = ga._generation
        population = ga._population

        parameters = {
            "generation": generation,
            "corner": [individual.param[0] for individual in population],
            "c": [individual.param[1] for individual in population],
            "a1": [individual.param[2] for individual in population],
            "a2": [individual.param[3] for individual in population],
            "b": [individual.param[4] for individual in population],
            "o": [individual.param[5] for individual in population],
            "x": [individual.param[6] for individual in population],
            "ww": [individual.param[7] for individual in population],
            "fitness": [individual.fitness() for individual in population],
        }

        with open(json_file, 'w') as f:
            json.dump(parameters, f)


if __name__ == '__main__':
    import timeit

    ga = GeneticAlgorithm('./ga_setting.json', Switch2_TW)
    elapsed_time = timeit.timeit('ga.run()', globals=globals(), number=1)

    print('>>>>>>>>>>>>>>>>>>>>>>>>>')
    print(ga.best)
    print(elapsed_time, '(s)')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>')
