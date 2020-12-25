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
    """Test3:generation_change
    """
    cnt = 0

    def __init__(self, parameter):
        self.parameter = parameter

    def fitness(self):
        return self.parameter

    def reset_fitness(self):
        print('reset')

    def is_optimal(self):
        return self.parameter == 9999

    @classmethod
    def random_instance(cls):
        instance = cls(cls.cnt)
        cls.cnt += 1
        return instance

    def crossover(self, other):
        return type(self)(100)

    def mutate(self):
        self.parameter = 999

    def large_mutate(self):
        self.parameter = 9999

    def save_population(self, fname):
        print(fname)

    def __str__(self):
        return "parameter=" + str(self.parameter)


class Test4(Test3):
    """Test4:mutate
    """
    cnt = 0


class Test5(Test3):
    """Test5:reset_fitness
    """
    cnt = 0


class Test6(Test3):
    """Test6:run
    """
    cnt = 0


class Test7(Test3):
    """Test7:run
    """
    cnt = 0

    def is_optimal(self):
        return self.parameter == 10000


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
            "max_generations": 3,
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

    def test_genetic_algorithm_mutate(self):
        ga = GeneticAlgorithm(self.json_file2, Test4)
        with captured_stdout() as stdout:
            ga._mutate()
        lines = stdout.getvalue().splitlines()
        expected = [' + mutate', ' + mutate']
        self.assertEqual(lines, expected)
        self.assertEqual([i.parameter for i in ga._population], [999, 999])

        ga._generation = ga._setting['large_mutation']
        with captured_stdout() as stdout:
            ga._mutate()
        lines = stdout.getvalue().splitlines()
        expected = [' + large_mutate', ' + large_mutate']
        self.assertEqual(lines, expected)
        self.assertEqual([i.parameter for i in ga._population], [9999, 9999])

    def test_genetic_algorithm_reset_fitness(self):
        ga = GeneticAlgorithm(self.json_file2, Test5)
        with captured_stdout() as stdout:
            ga._reset_fitness()
        lines = stdout.getvalue().splitlines()
        expected = ['reset', 'reset']
        self.assertEqual(lines, expected)

    def test_genetic_algorithm_run(self):
        # found optimal
        ga = GeneticAlgorithm(self.json_file2, Test6)
        with captured_stdout() as stdout:
            result = ga.run()
        lines = stdout.getvalue().splitlines()
        expected = """
Generation 0 Best 1 Avg 0.5
best: parameter=1

./population0.json
 + mutate
 + mutate
reset
reset
Generation 1 Best 999 Avg 999
best: parameter=999

./population1.json
 + large_mutate
 + large_mutate
reset
reset
Generation 2 Best 9999 Avg 9999
best: parameter=9999

----- optimal pattern is found! -----
./population.json
""".split('\n')[1:-1]
        self.assertEqual(lines, expected)
        self.assertEqual(str(result), 'parameter=9999')

        # not found optimal
        ga = GeneticAlgorithm(self.json_file2, Test7)
        with captured_stdout() as stdout:
            result = ga.run()
        lines = stdout.getvalue().splitlines()
        expected = """
Generation 0 Best 1 Avg 0.5
best: parameter=1

./population0.json
 + mutate
 + mutate
reset
reset
Generation 1 Best 999 Avg 999
best: parameter=999

./population1.json
 + large_mutate
 + large_mutate
reset
reset
Generation 2 Best 9999 Avg 9999
best: parameter=9999

./population2.json
 + mutate
 + mutate
reset
reset
Generation 3 Best 999 Avg 999
./population.json
""".split('\n')[1:-1]
        self.assertEqual(lines, expected)
        self.assertEqual(str(result), 'parameter=999')

    def test_genetic_algorithm_randomsum77(self):
        ga = GeneticAlgorithm(self.json_file, RandomSum77)
        result = ga.run()
        print('result:', result)

        self.assertTrue("parameter=77" in str(result))

    def test_genetic_algorithm_test(self):
        test1 = Test1(10)
        self.assertEqual(test1.fitness(), 10)
        self.assertIsNone(test1.reset_fitness())
        self.assertIsNone(test1.is_optimal())
        self.assertIsNone(test1.crossover(None))
        self.assertIsNone(test1.mutate())
        self.assertIsNone(test1.large_mutate())

        test2 = Test2(10)
        self.assertIsNone(test2.reset_fitness())
        self.assertIsNone(test2.is_optimal())
        self.assertIsNone(test2.crossover(None))
        self.assertIsNone(test2.mutate())
        self.assertIsNone(test2.large_mutate())

        randomsum77 = RandomSum77(10)
        randomsum77.mutate()
        self.assertEqual(randomsum77.parameter, 11)
        randomsum77.large_mutate()
        self.assertGreaterEqual(randomsum77.parameter, 0)
        self.assertLess(randomsum77.parameter, 100)
        self.assertEqual(randomsum77.name, str(randomsum77.parameter))
