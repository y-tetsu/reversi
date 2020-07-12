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
        8. Repeat 2. to 7. a certain number of times.

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
        You need to set the following parameters.
            max_generation       : Maximum number of generations to run the simulation
            population_num       : Number of populations.
            offspring_num        : Number of offsprings.
            mutation_chance      : The probability of a mutation occurring (1=100%)
            mutation_value       : The size of the parameter to vary in case of a mutation
            large_mutation       : Number of generations in which a large mutation always occurs
            large_mutation_value : The size of the parameter to vary in case of a large mutation
            board_size           : select board size (even number from 4 to 26)
            matches              : number of matches for estimating fitness
            threshold            : Fitness threshold for completion of the calculation
            random_opening       : number of turns in the early stages of random moves
            process              : number of distributed processing(max == 2)
"""

import os
import json
from random import randrange, random, randint
from copy import deepcopy

from reversi.genetic_algorithm import GeneticAlgorithm, Chromosome
from reversi import Simulator
from reversi.strategies.table import Table


MAX_WEIGHT = 250


class GeneticTable(Chromosome):
    """Discover parameter for Table-strategy"""
    def __init__(self, corner=None, c=None, a1=None, a2=None, b1=None, b2=None, b3=None, x=None, o1=None, o2=None):
        self.setting = self._load_setting('./ga_setting.json')
        self.param = [corner, c, a1, a2, b1, b2, b3, x, o1, o2]
        self.fitness_value = None

    def _load_setting(self, setting_json):
        """load setting"""
        setting = {}

        if setting_json is not None and os.path.isfile(setting_json):
            with open(setting_json) as f:
                setting = json.load(f)

        return setting

    def fitness(self):
        """fitness"""
        if self.fitness_value is not None:
            return self.fitness_value

        simulator = Simulator(
            {
                'Challenger': Table(
                    corner=self.param[0],
                    c=self.param[1],
                    a1=self.param[2],
                    a2=self.param[3],
                    b1=self.param[4],
                    b2=self.param[5],
                    b3=self.param[6],
                    x=self.param[7],
                    o1=self.param[8],
                    o2=self.param[9],
                ),
                'Opponent': Table(),
            },
            './ga_setting.json',
        )

        simulator.start()
        print(simulator)
        self.fitness_value = ((simulator.result_ratio['Challenger'] - simulator.result_ratio['Opponent']) + 100) / 2

        return self.fitness_value

    def reset_fitness(self):
        """reset fitness"""
        self.fitness_value = None

    def is_optimal(self):
        """check optimal"""
        return self.fitness() >= self.setting['threshold']

    @classmethod
    def random_instance(cls):
        """initial instance"""
        corner = randrange(MAX_WEIGHT) * (1 if random() > 0.5 else -1)
        c = randrange(MAX_WEIGHT) * (1 if random() > 0.5 else -1)
        a1 = randrange(MAX_WEIGHT) * (1 if random() > 0.5 else -1)
        a2 = randrange(MAX_WEIGHT) * (1 if random() > 0.5 else -1)
        b1 = randrange(MAX_WEIGHT) * (1 if random() > 0.5 else -1)
        b2 = randrange(MAX_WEIGHT) * (1 if random() > 0.5 else -1)
        b3 = randrange(MAX_WEIGHT) * (1 if random() > 0.5 else -1)
        x = randrange(MAX_WEIGHT) * (1 if random() > 0.5 else -1)
        o1 = randrange(MAX_WEIGHT) * (1 if random() > 0.5 else -1)
        o2 = randrange(MAX_WEIGHT) * (1 if random() > 0.5 else -1)

        return GeneticTable(corner=corner, c=c, a1=a1, a2=a2, b1=b1, b2=b2, b3=b3, x=x, o1=o1, o2=o2)

    def crossover(self, other):
        """crossover"""
        num1, num2 = randrange(10), randrange(10)
        (num1, num2) = (num1, num2) if num1 < num2 else (num2, num1)

        child = deepcopy(self) if random() > 0.5 else deepcopy(other)
        child.reset_fitness()

        for i in range(num1, num2+1):
            low, high = self.param[i], other.param[i]
            (low, high) = (low, high) if low < high else (high, low)
            child.param[i] = randint(low, high)

        return child

    def mutate(self):
        """mutate"""
        self.param[randrange(10)] += self.setting['mutation_value'] * (1 if random() > 0.5 else -1)

    def large_mutate(self):
        """large mutate"""
        self.param[randrange(10)] += self.setting['large_mutation_value'] * (1 if random() > 0.5 else -1)

    def __str__(self):
        return f"corner: {self.param[0]}\nc: {self.param[1]}\na1: {self.param[2]}\na2: {self.param[3]}\nb1: {self.param[4]}\nb2: {self.param[5]}\nb3: {self.param[6]}\nx: {self.param[7]}\no1: {self.param[8]}\no2: {self.param[9]}\nFitness: {self.fitness()}"  # noqa: E501

    @classmethod
    def load_population(cls, json_file):
        """load population"""
        generation, population = 0, {}

        if json_file is not None and os.path.isfile(json_file):
            with open(json_file) as f:
                json_setting = json.load(f)

                generation = json_setting["generation"]
                corner = json_setting["corner"]
                c = json_setting["c"]
                a1 = json_setting["a1"]
                a2 = json_setting["a2"]
                b1 = json_setting["b1"]
                b2 = json_setting["b2"]
                b3 = json_setting["b3"]
                x = json_setting["x"]
                o1 = json_setting["o1"]
                o2 = json_setting["o2"]

                population = [GeneticTable(corner=corner[i], c=c[i], a1=a1[i], a2=a2[i], b1=b1[i], b2=b2[i], b3=b3[i], x=x[i], o1=o1[i], o2=o2[i]) for i in range(len(corner))]  # noqa: E501

        return generation, population

    @classmethod
    def save_population(cls, ga, json_file):
        """save population"""
        generation = ga._generation
        population = ga._population

        parameters = {
            "generation": generation,
            "corner": [individual.param[0] for individual in population],
            "c": [individual.param[1] for individual in population],
            "a1": [individual.param[2] for individual in population],
            "a2": [individual.param[3] for individual in population],
            "b1": [individual.param[4] for individual in population],
            "b2": [individual.param[5] for individual in population],
            "b3": [individual.param[6] for individual in population],
            "x": [individual.param[7] for individual in population],
            "o1": [individual.param[8] for individual in population],
            "o2": [individual.param[9] for individual in population],
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
