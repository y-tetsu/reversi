#!/usr/bin/env python
"""
Switch_Evaluator_TPWEのパラメータ調整
"""
import sys
sys.path.append('../../')

import os
import json
from random import randrange, random
from copy import deepcopy

from chromosome import Chromosome
from genetic_algorithm import GeneticAlgorithm

from strategies.switch import Switch
from strategies import MinMax2Ro_TPWE
from strategies.minmax import MinMax2_TPWE
from strategies.coordinator import Evaluator_TPWE
from player import Player
from simulator import Simulator


class Switch_Evaluator_TPWE(Chromosome):
    """
    Switch_Evaluator_TPWEのパラメータ調整
    """
    def __init__(self, corner=None, c=None, a1=None, a2=None, b=None, x=None, o=None, wp=None, ww=None, we=None):
        self.setting = self._load_setting('./switch_setting.json')
        self.corner = corner
        self.c = c
        self.a1 = a1
        self.a2 = a2
        self.b = b
        self.x = x
        self.o = o
        self.wp = wp
        self.ww = ww
        self.we = we
        self.fitness_value = None

    def _load_setting(self, setting_json):
        """
        設定値読み込み
        """
        setting = {
            "turns": [36, 48, 60],
            "threshold": 60,
            "mutation_value": 1,
            "large_mutation_value": 10,
            "board_size": 8,
            "matches": 5,
            "board_type": "bitboard",
            "processes": 2
        }

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

        # 遺伝個体(2手読みSwitch-Edge)
        challenger = Switch(
            turns=[36, 48, 60],
            strategies=[
                MinMax2Ro_TPWE(
                    base=MinMax2_TPWE(
                        evaluator=Evaluator_TPWE(
                            corner=self.corner[i],
                            c=self.c[i],
                            a1=self.a1[i],
                            a2=self.a2[i],
                            b=self.b[i],
                            o=self.o[i],
                            x=self.x[i],
                            wp=self.wp[i],
                            ww=self.ww[i],
                            we=self.we[i]
                        )
                    )
                ) for i in range(len(self.setting['turns']))
            ]
        )

        # 対戦相手(2手読みEdge)
        opponent = MinMax2Ro_TPWE()

        # シミュレータ準備
        strategy_list = {
            'Challenger': challenger,
            'Opponent': opponent,
        }
        black_players = [Player('black', c, strategy_list[c]) for c in ['Challenger', 'Opponent']]
        white_players = [Player('white', c, strategy_list[c]) for c in ['Challenger', 'Opponent']]
        simulator = Simulator(
            black_players,
            white_players,
            self.setting['matches'],
            self.setting['board_size'],
            self.setting['board_type'],
            self.setting['processes']
        )

        # 2手読みのEdgeと対戦させ勝率を返す
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
        return self.fitness() >= self.setting["threshold"]

    @classmethod
    def random_instance(cls):
        """
        初期パラメータ設定
        """
        switch_num = len(Switch_Evaluator_TPWE().setting["turns"])

        corner_sign = 1 if random() > 0.5 else -1
        c_sign = 1 if random() > 0.5 else -1
        a1_sign = 1 if random() > 0.5 else -1
        a2_sign = 1 if random() > 0.5 else -1
        b_sign = 1 if random() > 0.5 else -1
        x_sign = 1 if random() > 0.5 else -1
        o_sign = 1 if random() > 0.5 else -1
        wp_sign = 1 if random() > 0.5 else -1
        we_sign = 1 if random() > 0.5 else -1

        corner = [randrange(200) * corner_sign for _ in range(switch_num)]
        c = [randrange(200) * c_sign for _ in range(switch_num)]
        a1 = [randrange(200) * a1_sign for _ in range(switch_num)]
        a2 = [randrange(200) * a2_sign for _ in range(switch_num)]
        b = [randrange(200) * b_sign for _ in range(switch_num)]
        x = [randrange(200) * x_sign for _ in range(switch_num)]
        o = [randrange(200) * o_sign for _ in range(switch_num)]
        wp = [randrange(200) * wp_sign for _ in range(switch_num)]
        ww = [10000 for _ in range(switch_num)]
        we = [randrange(200) * we_sign for _ in range(switch_num)]

        return Switch_Evaluator_TPWE(corner, c, a1, a2, b, x, o, wp, ww, we)

    def crossover(self, other):
        """
        二点交叉
        """
        num1, num2 = randrange(9), randrange(9)
        (num1, num2) = (num1, num2) if num1 < num2 else (num2, num1)

        population_num = len(self.corner)
        num3, num4 = randrange(population_num), randrange(population_num)
        (num3, num4) = (num3, num4) if num3 < num4 else (num3, num4)

        child1 = deepcopy(self)
        child1.reset_fitness()

        child2 = deepcopy(other)
        child2.reset_fitness()

        if num1 <= 0 and num2 >= 0:
            child1.corner[num3:num4+1] = other.corner[num3:num4+1]
            child2.corner[num3:num4+1] = self.corner[num3:num4+1]
        if num1 <= 1 and num2 >= 1:
            child1.c[num3:num4+1] = other.c[num3:num4+1]
            child2.c[num3:num4+1] = self.c[num3:num4+1]
        if num1 <= 2 and num2 >= 2:
            child1.a1[num3:num4+1] = other.a1[num3:num4+1]
            child2.a1[num3:num4+1] = self.a1[num3:num4+1]
        if num1 <= 3 and num2 >= 3:
            child1.a2[num3:num4+1] = other.a2[num3:num4+1]
            child2.a2[num3:num4+1] = self.a2[num3:num4+1]
        if num1 <= 4 and num2 >= 4:
            child1.b[num3:num4+1] = other.b[num3:num4+1]
            child2.b[num3:num4+1] = self.b[num3:num4+1]
        if num1 <= 5 and num2 >= 5:
            child1.x[num3:num4+1] = other.x[num3:num4+1]
            child2.x[num3:num4+1] = self.x[num3:num4+1]
        if num1 <= 6 and num2 >= 6:
            child1.o[num3:num4+1] = other.o[num3:num4+1]
            child2.o[num3:num4+1] = self.o[num3:num4+1]
        if num1 <= 7 and num2 >= 7:
            child1.wp[num3:num4+1] = other.wp[num3:num4+1]
            child2.wp[num3:num4+1] = self.wp[num3:num4+1]
        if num1 <= 8 and num2 >= 8:
            child1.we[num3:num4+1] = other.we[num3:num4+1]
            child2.we[num3:num4+1] = self.we[num3:num4+1]

        return child1 if random() > 0.5 else child2

    def mutate(self):
        """
        変異(摂動)
        """
        parameter_index = randrange(9)
        switch_num = len(self.setting["turns"])
        stage_index = randrange(switch_num)
        sign = 1 if random() > 0.5 else -1
        mutation_value = self.setting["mutation_value"]

        if parameter_index == 0:
            self.corner[stage_index] += mutation_value * sign
        elif parameter_index == 1:
            self.c[stage_index] += mutation_value * sign
        elif parameter_index == 2:
            self.a1[stage_index] += mutation_value * sign
        elif parameter_index == 3:
            self.a2[stage_index] += mutation_value * sign
        elif parameter_index == 4:
            self.b[stage_index] += mutation_value * sign
        elif parameter_index == 5:
            self.o[stage_index] += mutation_value * sign
        elif parameter_index == 6:
            self.x[stage_index] += mutation_value * sign
        elif parameter_index == 7:
            self.wp[stage_index] += mutation_value * sign
        elif parameter_index == 8:
            self.we[stage_index] += mutation_value * sign

    def large_mutate(self):
        """
        大変異(摂動)
        """
        parameter_index = randrange(9)
        switch_num = len(self.setting["turns"])
        stage_index = randrange(switch_num)
        sign = 1 if random() > 0.5 else -1
        large_mutation_value = self.setting["large_mutation_value"]

        if parameter_index == 0:
            self.corner[stage_index] += large_mutation_value * sign
        elif parameter_index == 1:
            self.c[stage_index] += large_mutation_value * sign
        elif parameter_index == 2:
            self.a1[stage_index] += large_mutation_value * sign
        elif parameter_index == 3:
            self.a2[stage_index] += large_mutation_value * sign
        elif parameter_index == 4:
            self.b[stage_index] += large_mutation_value * sign
        elif parameter_index == 5:
            self.o[stage_index] += large_mutation_value * sign
        elif parameter_index == 6:
            self.x[stage_index] += large_mutation_value * sign
        elif parameter_index == 7:
            self.wp[stage_index] += large_mutation_value * sign
        elif parameter_index == 8:
            self.we[stage_index] += large_mutation_value * sign

    def __str__(self):
        return f"corner: {self.corner}\nc: {self.c}\na1: {self.a1}\na2: {self.a2}\nb: {self.b}\no: {self.o}\nx: {self.x}\nwp: {self.wp}\nww: {self.ww}\nwe: {self.we}\nFitness: {self.fitness()}"

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
                corner = json_setting["corner"]
                c = json_setting["c"]
                a1 = json_setting["a1"]
                a2 = json_setting["a2"]
                b = json_setting["b"]
                o = json_setting["o"]
                x = json_setting["x"]
                wp = json_setting["wp"]
                ww = json_setting["ww"]
                we = json_setting["we"]

                population = [Switch_Evaluator_TPWE(corner[i], c[i], a1[i], a2[i], b[i], x[i], o[i], wp[i], ww[i], we[i]) for i in range(len(corner))]

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
            "corner": [individual.corner for individual in population],
            "c": [individual.c for individual in population],
            "a1": [individual.a1 for individual in population],
            "a2": [individual.a2 for individual in population],
            "b": [individual.b for individual in population],
            "o": [individual.o for individual in population],
            "x": [individual.x for individual in population],
            "wp": [individual.wp for individual in population],
            "ww": [individual.ww for individual in population],
            "we": [individual.we for individual in population],
            "fitness": [individual.fitness() for individual in population],
        }

        with open(json_file, 'w') as f:
            json.dump(parameters, f)


if __name__ == '__main__':
    import timeit

    ga = GeneticAlgorithm('./ga_setting.json', Switch_Evaluator_TPWE)
    elapsed_time = timeit.timeit('ga.run()', globals=globals(), number=1)

    print('>>>>>>>>>>>>>>>>>>>>>>>>>')
    print(ga.best)
    print(elapsed_time, '(s)')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>')
