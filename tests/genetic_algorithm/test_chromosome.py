"""Tests of chromosome.py
"""

import unittest

from reversi.genetic_algorithm import Chromosome


class TestChromosome(unittest.TestCase):
    """chromosome
    """
    def test_chromosome(self):
        Chromosome.fitness("self")
        Chromosome.reset_fitness("self")
        Chromosome.is_optimal("self")
        Chromosome.random_instance()
        Chromosome.crossover("self", "other")
        Chromosome.mutate("self")
        Chromosome.large_mutate("self")

        with self.assertRaises(TypeError):
            class Test(Chromosome):
                pass
            test = Test()

        with self.assertRaises(TypeError):
            class Test(Chromosome):
                def reset_fitness(self):
                    pass

                def is_optimal(self):
                    pass

                def random_instance(cls):
                    pass

                def crossover(self, other):
                    pass

                def mutate(self):
                    pass

                def large_mutate(self):
                    pass

            Test.reset_fitness("self")
            Test.is_optimal("self")
            Test.random_instance("cls")
            Test.crossover("self", "other")
            Test.mutate("self")
            Test.large_mutate("self")

            test = Test()

        with self.assertRaises(TypeError):
            class Test(Chromosome):
                def fitness(self):
                    pass

                def is_optimal(self):
                    pass

                def random_instance(cls):
                    pass

                def crossover(self, other):
                    pass

                def mutate(self):
                    pass

                def large_mutate(self):
                    pass

            Test.fitness("self")
            Test.is_optimal("self")
            Test.random_instance("cls")
            Test.crossover("self", "other")
            Test.mutate("self")
            Test.large_mutate("self")

            test = Test()

        with self.assertRaises(TypeError):
            class Test(Chromosome):
                def fitness(self):
                    pass

                def reset_fitness(self):
                    pass

                def random_instance(cls):
                    pass

                def crossover(self, other):
                    pass

                def mutate(self):
                    pass

                def large_mutate(self):
                    pass

            Test.fitness("self")
            Test.reset_fitness("self")
            Test.random_instance("cls")
            Test.crossover("self", "other")
            Test.mutate("self")
            Test.large_mutate("self")

            test = Test()

        with self.assertRaises(TypeError):
            class Test(Chromosome):
                def fitness(self):
                    pass

                def reset_fitness(self):
                    pass

                def is_optimal(self):
                    pass

                def crossover(self, other):
                    pass

                def mutate(self):
                    pass

                def large_mutate(self):
                    pass

            Test.fitness("self")
            Test.reset_fitness("self")
            Test.is_optimal("self")
            Test.crossover("self", "other")
            Test.mutate("self")
            Test.large_mutate("self")

            test = Test()

        with self.assertRaises(TypeError):
            class Test(Chromosome):
                def fitness(self):
                    pass

                def reset_fitness(self):
                    pass

                def is_optimal(self):
                    pass

                def random_instance(cls):
                    pass

                def mutate(self):
                    pass

                def large_mutate(self):
                    pass

            Test.fitness("self")
            Test.reset_fitness("self")
            Test.is_optimal("self")
            Test.random_instance("cls")
            Test.mutate("self")
            Test.large_mutate("self")

            test = Test()

        with self.assertRaises(TypeError):
            class Test(Chromosome):
                def fitness(self):
                    pass

                def reset_fitness(self):
                    pass

                def is_optimal(self):
                    pass

                def random_instance(cls):
                    pass

                def crossover(self, other):
                    pass

                def large_mutate(self):
                    pass

            Test.fitness("self")
            Test.reset_fitness("self")
            Test.is_optimal("self")
            Test.random_instance("cls")
            Test.crossover("self", "other")
            Test.large_mutate("self")

            test = Test()

        with self.assertRaises(TypeError):
            class Test(Chromosome):
                def fitness(self):
                    pass

                def reset_fitness(self):
                    pass

                def is_optimal(self):
                    pass

                def random_instance(cls):
                    pass

                def crossover(self, other):
                    pass

                def mutate(self):
                    pass

            Test.fitness("self")
            Test.reset_fitness("self")
            Test.is_optimal("self")
            Test.random_instance("cls")
            Test.crossover("self", "other")
            Test.mutate("self")

            test = Test()

        class Test(Chromosome):
            def fitness(self):
                pass

            def reset_fitness(self):
                pass

            def is_optimal(self):
                pass

            def random_instance(cls):
                pass

            def crossover(self, other):
                pass

            def mutate(self):
                pass

            def large_mutate(self):
                pass

        Test.fitness("self")
        Test.reset_fitness("self")
        Test.is_optimal("self")
        Test.random_instance("cls")
        Test.crossover("self", "other")
        Test.mutate("self")
        Test.large_mutate("self")

        test = Test()
        self.assertIsInstance(test, Test)
