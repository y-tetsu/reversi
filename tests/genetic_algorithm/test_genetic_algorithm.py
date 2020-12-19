"""Tests of genetic_algorithm.py
"""

import unittest
from test.support import captured_stdout
import os
import json
from random import randrange
from copy import deepcopy

from reversi.genetic_algorithm import Chromosome, GeneticAlgorithm


class Test1(Chromosome):
    """Test1:without load_population
    """
    cnt = 0

    def __init__(self, parameter):
        self.parameter = parameter

    def fitness(self):
        return self.parameter

    def reset_fitness(self):
        pass

    def is_optimal(self):
        pass

    @classmethod
    def random_instance(cls):
        instance = Test1(Test1.cnt)
        Test1.cnt += 1
        return instance

    def crossover(self, other):
        pass

    def mutate(self):
        pass

    def large_mutate(self):
        pass


class Test2(Chromosome):
    """Test2:with load_population
    """
    cnt = 0

    def __init__(self, parameter):
        self.parameter = parameter

    def fitness(self):
        return self.parameter

    def reset_fitness(self):
        pass

    def is_optimal(self):
        pass

    @classmethod
    def random_instance(cls):
        instance = Test2(Test2.cnt)
        Test2.cnt += 1
        return instance

    def crossover(self, other):
        pass

    def mutate(self):
        pass

    def large_mutate(self):
        pass

    @classmethod
    def load_population(cls, json_file):
        generation, population = 0, {}

        if json_file is not None and os.path.isfile(json_file):
            with open(json_file) as f:
                json_setting = json.load(f)

                generation = json_setting["generation"]
                parameter = json_setting["parameter"]

                population = [Test2(parameter=parameter[i]) for i in range(len(parameter))]

        return generation, population


class Test3(Chromosome):
    """Test3:cross_over
    """
    cnt = 0

    def __init__(self, parameter):
        self.parameter = parameter

    def fitness(self):
        return self.parameter

    def reset_fitness(self):
        pass

    def is_optimal(self):
        pass

    @classmethod
    def random_instance(cls):
        instance = Test3(Test3.cnt)
        Test3.cnt += 1
        return instance

    def crossover(self, other):
        return Test3(100)

    def mutate(self):
        pass

    def large_mutate(self):
        pass


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


class TestGeneticAlgorithm(unittest.TestCase):
    """GeneticAlgorithm
    """
    def setUp(self):
        self.json_file = './ga_setting.json'
        self.ga_setting = {
            "population_num": 10,
            "offspring_num": 5,
            "max_generations": 10000,
            "mutation_chance": 0.2,
            "large_mutation": 100
        }
        with open(self.json_file, 'w') as f:
            json.dump(self.ga_setting, f)

        self.json_file2 = './ga_setting2.json'
        self.ga_setting2 = {
            "population_num": 2,
            "offspring_num": 2,
            "max_generations": 10000,
            "mutation_chance": 1,
            "large_mutation": 2
        }
        with open(self.json_file2, 'w') as f:
            json.dump(self.ga_setting2, f)

        self.population_json = './population.json'
        self.populations1 = {
            "generation": 3,
            "parameter": [0, 1, 2]
        }
        self.populations2 = {
            "generation": 10,
            "parameter": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        }

    def tearDown(self):
        os.remove(self.json_file)

    def test_genetic_algorithm_init(self):
        with captured_stdout() as stdout:
            ga = GeneticAlgorithm(self.json_file, Test1)

        lines = stdout.getvalue().splitlines()
        expected = ['[random_instance]']
        self.assertEqual(lines, expected)
        self.assertEqual(ga._setting, self.ga_setting)
        self.assertEqual(ga._generation, 0)
        for i in range(ga._setting["population_num"]):
            self.assertEqual(ga._population[i].parameter, i)
        self.assertEqual(ga._fitness_key, Test1.fitness)
        self.assertIsNone(ga.best)

    def test_genetic_algorithm_init_with_population(self):
        with open(self.population_json, 'w') as f:
            json.dump(self.populations1, f)

        with captured_stdout() as stdout:
            ga = GeneticAlgorithm(self.json_file, Test1)

        os.remove(self.population_json)

        lines = stdout.getvalue().splitlines()
        expected = ['[random_instance]']
        self.assertEqual(lines, expected)
        self.assertEqual(ga._setting, self.ga_setting)
        self.assertEqual(ga._generation, 0)
        for i in range(ga._setting["population_num"]):
            self.assertEqual(ga._population[i].parameter, i+10)
        self.assertEqual(ga._fitness_key, Test1.fitness)
        self.assertIsNone(ga.best)

    def test_genetic_algorithm_init_with_population_expansion(self):
        with open(self.population_json, 'w') as f:
            json.dump(self.populations1, f)

        with captured_stdout() as stdout:
            ga = GeneticAlgorithm(self.json_file, Test2)

        os.remove(self.population_json)

        lines = stdout.getvalue().splitlines()
        expected = ['[load_population]', ' - expansion']
        self.assertEqual(lines, expected)
        self.assertEqual(ga._generation, 3)
        self.assertEqual(len(ga._population), ga._setting["population_num"])
        self.assertEqual([i.parameter for i in ga._population], [0, 1, 2, 10, 11, 12, 13, 14, 15, 16])

    def test_genetic_algorithm_init_with_population_reduction(self):
        with open(self.population_json, 'w') as f:
            json.dump(self.populations2, f)

        with captured_stdout() as stdout:
            ga = GeneticAlgorithm(self.json_file, Test2)

        os.remove(self.population_json)

        lines = stdout.getvalue().splitlines()
        expected = ['[load_population]', ' - reduction']
        self.assertEqual(lines, expected)
        self.assertEqual(ga._generation, 10)
        self.assertEqual(len(ga._population), ga._setting["population_num"])
        self.assertEqual([i.parameter for i in ga._population], [12, 11, 10, 9, 8, 7, 6, 5, 4, 3])

    def test_genetic_algorithm_generation_change(self):
        ga = GeneticAlgorithm(self.json_file2, Test3)
        ga._generation_change()
        self.assertEqual([i.parameter for i in ga._population], [100, 100])

    def test_genetic_algorithm_randomsum77(self):
        ga = GeneticAlgorithm(self.json_file, RandomSum77)
        result = ga.run()
        print('result:', result)

        self.assertTrue("parameter=77" in str(result))
