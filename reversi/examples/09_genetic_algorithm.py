#!/usr/bin/env python
"""A example of Genetic Algorithm for reversi

    This example uses a genetic algorithm to discover the optimal weights for a Table-strategy.
    This is achieved by implementing GeneticTable, which inherits from the Chromosome class.

    genetic algorithm flow:
        1. Prepare a population that generated individuals with random parameters.
        2. Check the fitness of all individuals, and exit when the fitness reaches threshold.
        3. Randomly select two parents from the population.
        4. Crossovering between the selected parents to generate a specified number of offspring.
        5. Find the fitness of all parent and offspring individuals.
           and select the two best fitted individuals to replace them.
        6. Mutations occur in each individual at a certain rate.
        7. In the case of certain generations, they generate large mutations.
        8. Repeat 2-7 a certain number of times.

    Inheritance of Chromosome class:
        You need to implement the following methods.
            fitness         : return fitness value
            reset_fitness   : clear fitness_value if you need
            is_optimal      : check if it is opptimal
            random_instance : initialize instance randomly
            crossover       : implement crossover
            mutate          : implement mutate
            large_mutate    : implement large mutate

    ga_setting.json format:
        population_num  : Number of populations.
        offspring_num   : Number of offsprings.
        max_generation  : Maximum number of generations to run the simulation
        mutation_chance : The probability of a mutation occurring (1=100%)
        large_mutation  : Number of generations in which a large mutation always occurs

    chromosome_setting.json format:
        threshold            : Fitness threshold for completion of the calculation
        mutatin_value        : The size of the parameter to vary in case of a mutation
        large_mutation_value : The size of the parameter to vary in case of a large mutation
        board_size           : select board size (even number from 4 to 26)
        board_type           : bitboard or board (bitboard is faster than board)
        matches              : number of matches for estimating fitness
        process              : number of distributed processing
        random_opening       : number of turns in the early stages of random moves
        characters           : select array "Challenger" and "Opponent"
"""

import os
import json
from random import randrange, random
from copy import deepcopy

from reversi.genetic_algorithm.genetic_algorithm import GeneticAlgorithm
from reversi.genetic_algorithm.chromosome import Chromosome
from reversi import Simulator
from reversi.strategies.table import Table


class GeneticTable(Chromosome):
    """Discover parameter for Table-strategy
    """
    def __init__(self, corner=None, c=None, a1=None, a2=None, b=None, x=None, o=None):
        self.setting = self._load_setting('./chromosome_setting.json')
        self.corner = corner
        self.c = c
        self.a1 = a1
        self.a2 = a2
        self.b = b
        self.x = x
        self.o = o
        self.fitness_value = None

    def _load_setting(self, setting_json):
        """load setting
        """
        setting = {
            "threshold": 75,
            "mutation_value": 3,
            "large_mutation_value": 25,
            "board_size": 8,
            "matches": 100,
            "board_type": "bitboard",
            "processes": 2,
            "random_opening": 8,
            "characters": [
                "Challenger",
                "Opponent"
            ]
        }

        if setting_json is not None and os.path.isfile(setting_json):
            with open(setting_json) as f:
                setting = json.load(f)

        return setting

    def fitness(self):
        """fitness
        """
        if self.fitness_value is not None:
            return self.fitness_value

        challenger = Table(
            corner=self.corner,
            c=self.c,
            a1=self.a1,
            a2=self.a2,
            b=self.b,
            o=self.o,
            x=self.x,
        )

        opponent = Table()

        simulator = Simulator(
            {
                'Challenger': challenger,
                'Opponent': opponent,
            },
            './chromosome_setting.json',
        )

        simulator.start()
        print(simulator)
        self.fitness_value = ((simulator.result_ratio['Challenger'] - simulator.result_ratio['Opponent']) + 100) / 2

        return self.fitness_value

    def reset_fitness(self):
        """reset fitness
        """
        self.fitness_value = None

    def is_optimal(self):
        """check optimal
        """
        return self.fitness() >= self.setting['threshold']

    @classmethod
    def random_instance(cls):
        """initial instance
        """
        max_range = 200

        corner = randrange(max_range) * (1 if random() > 0.5 else -1)
        c = randrange(max_range) * (1 if random() > 0.5 else -1)
        a1 = randrange(max_range) * (1 if random() > 0.5 else -1)
        a2 = randrange(max_range) * (1 if random() > 0.5 else -1)
        b = randrange(max_range) * (1 if random() > 0.5 else -1)
        x = randrange(max_range) * (1 if random() > 0.5 else -1)
        o = randrange(max_range) * (1 if random() > 0.5 else -1)

        return GeneticTable(corner, c, a1, a2, b, x, o)

    def crossover(self, other):
        """crossover
        """
        num1, num2 = randrange(7), randrange(7)
        (num1, num2) = (num1, num2) if num1 < num2 else (num2, num1)

        child1 = deepcopy(self)
        child1.reset_fitness()

        child2 = deepcopy(other)
        child2.reset_fitness()

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

        return child1 if random() > 0.5 else child2

    def mutate(self):
        """mutate
        """
        parameter_index = randrange(7)
        sign = 1 if random() > 0.5 else -1
        mutation_value = self.setting['mutation_value']

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

    def large_mutate(self):
        """large mutate
        """
        parameter_index = randrange(7)
        sign = 1 if random() > 0.5 else -1
        large_mutation_value = self.setting['large_mutation_value']

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

    def __str__(self):
        return f"corner: {self.corner}\nc: {self.c}\na1: {self.a1}\na2: {self.a2}\nb: {self.b}\no: {self.o}\nx: {self.x}\nFitness: {self.fitness()}"

    @classmethod
    def load_population(cls, json_file):
        """load population
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

                population = [GeneticTable(corner[i], c[i], a1[i], a2[i], b[i], x[i], o[i], wp[i], ww[i], we[i]) for i in range(len(corner))]

        return generation, population

    @classmethod
    def save_population(cls, ga, json_file):
        """save population
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
            "fitness": [individual.fitness() for individual in population],
        }

        with open(json_file, 'w') as f:
            json.dump(parameters, f)


if __name__ == '__main__':
    import timeit

    ga = GeneticAlgorithm('./ga_setting.json', GeneticTable)
    elapsed_time = timeit.timeit('ga.run()', globals=globals(), number=1)

    print('>>>>>>>>>>>>>>>>>>>>>>>>>')
    print(ga.best)
    print(elapsed_time, '(s)')
    print('>>>>>>>>>>>>>>>>>>>>>>>>>')
