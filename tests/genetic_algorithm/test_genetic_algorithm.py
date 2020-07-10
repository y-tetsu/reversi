"""Tests of genetic_algorithm.py
"""

import unittest
import os
import json
from random import randrange
from copy import deepcopy

from reversi.genetic_algorithm import Chromosome, GeneticAlgorithm


class TestGeneticAlgorithm(unittest.TestCase):
    """GeneticAlgorithm
    """
    def test_genetic_algorithm_randomsum77(self):
        class RandomSum77(Chromosome):
            """RandomSum77
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
                return RandomSum77(randrange(100))

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

        json_file = './ga_setting.json'

        ga_setting = {
            "population_num": 10,
            "offspring_num": 5,
            "max_generations": 10000,
            "mutation_chance": 0.2,
            "large_mutation": 100
        }

        with open(json_file, 'w') as f:
            json.dump(ga_setting, f)

        ga = GeneticAlgorithm(json_file, RandomSum77)
        result = ga.run()
        print('result:', result)

        os.remove(json_file)

        self.assertTrue("parameter=77" in str(result))
