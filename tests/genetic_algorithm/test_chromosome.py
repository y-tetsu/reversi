"""Tests of chromosome.py
"""

import unittest

from reversi.genetic_algorithm import Chromosome


class TestChromosome(unittest.TestCase):
    """chromosome
    """
    def test_chromosome(self):
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

        test = Test()
        self.assertIsInstance(test, Test)
