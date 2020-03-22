#!/usr/bin/env python
"""
染色体基底クラス
"""
import abc


class Chromosome(metaclass=abc.ABCMeta):
    """
    染色体基底クラス
    """
    @abc.abstractmethod
    def fitness(self):
        pass

    @abc.abstractmethod
    def reset_fitness(self):
        pass

    @classmethod
    @abc.abstractmethod
    def random_instance(cls):
        pass

    @abc.abstractmethod
    def crossover(self, other):
        pass

    @abc.abstractmethod
    def mutate(self):
        pass

    @abc.abstractmethod
    def large_mutate(self):
        pass
