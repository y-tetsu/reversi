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


SWITCH_NUM = 5
POPULATION_NUM = 3


class Switch_Evaluator_TPWE(Chromosome):
    """
    Switch_Evaluator_TPWEのパラメータ調整
    """
    def __init__(self, corner, c, a1, a2, b, x, o, wp, ww, we):
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

    def fitness(self):
        """
        適応度
        """
        if self.fitness_value:
            return self.fitness_value

        # 自分
        challenger = Switch(
            turns=[
                12,
                24,
                36,
                48,
                60
            ],
            strategies=[
                MinMax2Ro_TPWE(base=MinMax2_TPWE(evaluator=Evaluator_TPWE(corner=self.corner[i], c=self.c[i], a1=self.a1[i], a2=self.a2[i], b=self.b[i], o=self.o[i], x=self.x[i], wp=self.wp[i], ww=self.ww[i], we=self.we[i]))) for i in range(SWITCH_NUM)
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
            15,
            8,
            "bitboard",
            2
        )

        # 2手読みのEdgeと対戦させ勝率を返す
        simulator.start()
        self.fitness = simulator.result_ratio['Challenger']

        return self.fitness

    def reset_fitness(self):
        """
        適応度のリセット
        """
        self.fitness_value = None

    @classmethod
    def random_instance(cls):
        """
        初期パラメータ設定
        """
        corner = [randrange(100) for _ in range(SWITCH_NUM)]
        c = [randrange(100) for _ in range(SWITCH_NUM)]
        a1 = [randrange(100) for _ in range(SWITCH_NUM)]
        a2 = [randrange(100) for _ in range(SWITCH_NUM)]
        b = [randrange(100) for _ in range(SWITCH_NUM)]
        x = [randrange(100) for _ in range(SWITCH_NUM)]
        o = [randrange(100) for _ in range(SWITCH_NUM)]
        wp = [randrange(100) for _ in range(SWITCH_NUM)]
        ww = [randrange(1000) for _ in range(SWITCH_NUM)]
        we = [randrange(100) for _ in range(SWITCH_NUM)]

        return Switch_Evaluator_TPWE(corner, c, a1, a2, b, x, o, wp, ww, we)

    def crossover(self, other):
        """
        二点交叉
        """
        num1, num2 = randrange(10), randrange(10)
        (num1, num2) = (num1, num2) if num1 < num2 else (num2, num1)

        child1 = deepcopy(self)
        child2 = deepcopy(other)

        if num1 <= 0 and num2 >= 0:
            child1.corner = other.corner
            child2.corner = self.corner

        if num1 <= 1 and num2 >= 1:
            child1.c = other.c
            child2.c = self.c

        if num1 <= 2 and num2 >= 2:
            child1.a1 = other.a1
            child2.a1 = self.a1

        if num1 <= 3 and num2 >= 3:
            child1.a2 = other.a2
            child2.a2 = self.a2

        if num1 <= 4 and num2 >= 4:
            child1.b = other.b
            child2.b = self.b

        if num1 <= 5 and num2 >= 5:
            child1.x = other.x
            child2.x = self.x

        if num1 <= 6 and num2 >= 6:
            child1.o = other.o
            child2.o = self.o

        if num1 <= 7 and num2 >= 7:
            child1.wp = other.wp
            child2.wp = self.wp

        if num1 <= 8 and num2 >= 8:
            child1.ww = other.ww
            child2.ww = self.ww

        if num1 <= 9 and num2 >= 9:
            child1.we = other.we
            child2.we = self.we

        return child1, child2

    def mutate(self):
        """
        変異(摂動)
        """
        parameter_index = randrange(10)
        stage_index = randrange(SWITCH_NUM)

        print(parameter_index, stage_index)

        if parameter_index == 0:
            if random() > 0.5:
                self.corner[stage_index] += 1
            else:
                self.corner[stage_index] -= 1
        elif parameter_index == 1:
            if random() > 0.5:
                self.c[stage_index] += 1
            else:
                self.c[stage_index] -= 1
        elif parameter_index == 2:
            if random() > 0.5:
                self.a1[stage_index] += 1
            else:
                self.a1[stage_index] -= 1
        elif parameter_index == 3:
            if random() > 0.5:
                self.a2[stage_index] += 1
            else:
                self.a2[stage_index] -= 1
        elif parameter_index == 4:
            if random() > 0.5:
                self.b[stage_index] += 1
            else:
                self.b[stage_index] -= 1
        elif parameter_index == 5:
            if random() > 0.5:
                self.o[stage_index] += 1
            else:
                self.o[stage_index] -= 1
        elif parameter_index == 6:
            if random() > 0.5:
                self.x[stage_index] += 1
            else:
                self.x[stage_index] -= 1
        elif parameter_index == 7:
            if random() > 0.5:
                self.wp[stage_index] += 1
            else:
                self.wp[stage_index] -= 1
        elif parameter_index == 8:
            if random() > 0.5:
                self.ww[stage_index] += 1
            else:
                self.ww[stage_index] -= 1
        elif parameter_index == 9:
            if random() > 0.5:
                self.we[stage_index] += 1
            else:
                self.we[stage_index] -= 1

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

                population = [Switch_Evaluator_TPWE(corner[i], c[i], a1[i], a2[i], b[i], x[i], o[i], wp[i], ww[i], we[i]) for i in range(POPULATION_NUM)]

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
            "corner": [population[i].corner for i in range(POPULATION_NUM)],
            "c": [population[i].c for i in range(POPULATION_NUM)],
            "a1": [population[i].a1 for i in range(POPULATION_NUM)],
            "a2": [population[i].a2 for i in range(POPULATION_NUM)],
            "b": [population[i].b for i in range(POPULATION_NUM)],
            "o": [population[i].o for i in range(POPULATION_NUM)],
            "x": [population[i].x for i in range(POPULATION_NUM)],
            "wp": [population[i].wp for i in range(POPULATION_NUM)],
            "ww": [population[i].ww for i in range(POPULATION_NUM)],
            "we": [population[i].we for i in range(POPULATION_NUM)],
        }

        with open(json_file, 'w') as f:
            json.dump(parameters, f)


if __name__ == '__main__':
    generation, population = 1, [Switch_Evaluator_TPWE.random_instance() for _ in range(POPULATION_NUM)]

    if os.path.isfile('./population.json'):
        generation, population = Switch_Evaluator_TPWE.load_population('./population.json')

    ga = GeneticAlgorithm(generation, population, './setting.json')
    #result = ga.run()
    #print(result)

    Switch_Evaluator_TPWE.save_population(ga, './population.json')
