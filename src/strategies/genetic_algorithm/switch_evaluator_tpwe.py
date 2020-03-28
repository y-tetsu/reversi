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
            # 48手-60手
            turns=[48, 60],
            strategies=[
                MinMax2Ro_TPWE(),
                MinMax2Ro_TPWE(
                    base=MinMax2_TPWE(
                        evaluator=Evaluator_TPWE(
                            corner=self.corner,
                            c=self.c,
                            a1=self.a1,
                            a2=self.a2,
                            b=self.b,
                            o=self.o,
                            x=self.x,
                            wp=self.wp,
                            ww=self.ww,
                            we=self.we
                        )
                    )
                )
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
        corner_sign = 1 if randrange(1) else -1
        c_sign = 1 if randrange(1) else -1
        a1_sign = 1 if randrange(1) else -1
        a2_sign = 1 if randrange(1) else -1
        b_sign = 1 if randrange(1) else -1
        x_sign = 1 if randrange(1) else -1
        o_sign = 1 if randrange(1) else -1
        wp_sign = 1 if randrange(1) else -1
        we_sign = 1 if randrange(1) else -1

        corner = randrange(200) * corner_sign
        c = randrange(200) * c_sign
        a1 = randrange(200) * a1_sign
        a2 = randrange(200) * a2_sign
        b = randrange(200) * b_sign
        x = randrange(200) * x_sign
        o = randrange(200) * o_sign
        wp = randrange(200) * wp_sign
        ww = 10000
        we = randrange(200) * we_sign

        return Switch_Evaluator_TPWE(corner, c, a1, a2, b, x, o, wp, ww, we)

    def crossover(self, other):
        """
        二点交叉
        """
        num1, num2 = randrange(9), randrange(9)
        (num1, num2) = (num1, num2) if num1 < num2 else (num2, num1)

        child = deepcopy(self)
        child.reset_fitness()

        if num1 <= 0 and num2 >= 0:
            child.corner = other.corner
        if num1 <= 1 and num2 >= 1:
            child.c = other.c
        if num1 <= 2 and num2 >= 2:
            child.a1 = other.a1
        if num1 <= 3 and num2 >= 3:
            child.a2 = other.a2
        if num1 <= 4 and num2 >= 4:
            child.b = other.b
        if num1 <= 5 and num2 >= 5:
            child.x = other.x
        if num1 <= 6 and num2 >= 6:
            child.o = other.o
        if num1 <= 7 and num2 >= 7:
            child.wp = other.wp
        if num1 <= 8 and num2 >= 8:
            child.we = other.we

        return child

    def mutate(self):
        """
        変異(摂動)
        """
        parameter_index = randrange(9)
        sign = 1 if random() > 0.5 else -1
        mutation_value = self.setting["mutation_value"]

        if parameter_index == 0:
            self.corner += mutation_value * sign
        elif parameter_index == 1:
            self.c += mutation_value * sign
        elif parameter_index == 2:
            self.a1 += mutation_value * sign
        elif parameter_index == 3:
            self.a2 += mutation_value * sign
        elif parameter_index == 4:
            self.b += mutation_value * sign
        elif parameter_index == 5:
            self.o += mutation_value * sign
        elif parameter_index == 6:
            self.x += mutation_value * sign
        elif parameter_index == 7:
            self.wp += mutation_value * sign
        elif parameter_index == 8:
            self.we += mutation_value * sign

    def large_mutate(self):
        """
        大変異(摂動)
        """
        parameter_index = randrange(9)
        sign = 1 if random() > 0.5 else -1
        large_mutation_value = self.setting["large_mutation_value"]

        if parameter_index == 0:
            self.corner += large_mutation_value * sign
        elif parameter_index == 1:
            self.c += large_mutation_value * sign
        elif parameter_index == 2:
            self.a1 += large_mutation_value * sign
        elif parameter_index == 3:
            self.a2 += large_mutation_value * sign
        elif parameter_index == 4:
            self.b += large_mutation_value * sign
        elif parameter_index == 5:
            self.o += large_mutation_value * sign
        elif parameter_index == 6:
            self.x += large_mutation_value * sign
        elif parameter_index == 7:
            self.wp += large_mutation_value * sign
        elif parameter_index == 8:
            self.we += large_mutation_value * sign

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

                population = [Switch_Evaluator_TPWE(corner[i], c[i], a1[i], a2[i], b[i], x[i], o[i], wp[i], ww[i], we[i]) for i in range(Switch_Evaluator_TPWE().setting["population_num"])]

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
