"""
Author: Cylix Lee (cylix.lee@foxmail.com).
Created on: March 12th, 2023

Genetic algorithm to solve the puzzle.

ATTENTION: This algorithm is theoretically correct, but due to lack of computing power, this algorithm has never given
    a decent solution. It may be not suitable for this puzzle scenario.
"""
from __future__ import annotations

import copy
import random

import matrix
from algorithm import SolutionAlgorithm, SolutionStep

POPULATION_SIZE = 32768
FINAL_ADAPTIVITY = 123456
CROSSOVER_RANGE = POPULATION_SIZE // 2
CROSSOVER_POSSIBILITY = 0.5
MUTATE_POSSIBILITY = 0.01
EVOLUTION_ROUND = 100


def positional_adaptivity(target: matrix.Matrix, ideal: matrix.Matrix) -> int:
    """
    Calculate one part of adaptivity based on positional arrangements.

    :param target: The current matrix
    :param ideal: The final matrix
    :return: part of adaptivity value
    """
    value = 0
    for i in range(matrix.MATRIX_SIZE):
        for j in range(matrix.MATRIX_SIZE):
            element = target.fetch(i, j)
            for m in range(matrix.MATRIX_SIZE):
                for n in range(matrix.MATRIX_SIZE):
                    if ideal.fetch(m, n) == element:
                        value -= (abs(i - m) + abs(j - n)) ** 2
    return value


class Individual:
    """
    A class representing an individual in a population, composed of genes and adaptivity.
    """

    def __init__(self, length: int) -> None:
        if length < 0:
            return
        self.gene = [random.choice(matrix.DIRECTIONS) for _ in range(length)]
        self.adaptivity = 0

    def __str__(self) -> str:
        result = ""
        for d in self.gene:
            if d == matrix.Direction.UP:
                result += "U"
            elif d == matrix.Direction.LEFT:
                result += "L"
            elif d == matrix.Direction.DOWN:
                result += "D"
            elif d == matrix.Direction.RIGHT:
                result += "R"
        return result

    def clone(self) -> Individual:
        result = Individual(-1)
        result.gene = copy.deepcopy(self.gene)
        result.adaptivity = copy.deepcopy(self.adaptivity)
        return result

    def calculate_adaptivity(self, initial: matrix.Matrix, final: matrix.Matrix) -> None:
        """
        Calculate the whole adaptivity based on positional arrangement and moving steps.

        :param initial: The initial matrix with no moving steps applied.
        :param final: The final matrix to compare.
        """
        self.adaptivity = 0
        candidate = initial.clone()
        last_candidate = candidate
        for i, direction in enumerate(self.gene):
            last_candidate = candidate
            candidate = candidate.play_only(direction)
            if candidate is None:
                self.adaptivity += i
                break
            if candidate == final:
                self.gene = self.gene[:i + 1]
                self.adaptivity = FINAL_ADAPTIVITY
                return
        self.adaptivity += positional_adaptivity(last_candidate, final)


class GeneticAlgorithm(SolutionAlgorithm):
    """
    The Genetic Algorithm class that performs evolution. Theoretically, this algorithm is suitable for situations in
    which human is difficult to find a decent solution. This class takes a depth limit too, as unlimited depth may
    cause the problem scale grow extremely.

    However, Genetic Algorithm is an algorithm requiring high computing power. Simultaneously, this puzzle is a large
    scaled problem in calculation. Thus, the algorithm has never given a decent solution so far.
    """

    def __init__(self, depth_limit: int, initial_matrix: matrix.Matrix, final_matrix: matrix.Matrix) -> None:
        super().__init__(initial_matrix, final_matrix)
        self.depth_limit = depth_limit
        self.population = [Individual(depth_limit) for _ in range(POPULATION_SIZE)]

    def __str__(self) -> str:
        return "depth-limited Genetic Algorithm (depth_limit={}, evolution_round={})".format(self.depth_limit,
                                                                                             EVOLUTION_ROUND)

    def solve(self) -> list[SolutionStep] | None:
        """
        Typical routine of genetic algorithm: select, crossover and mutate. Evaluation is performed before all those
        steps.

        :return: A list containing steps to solve the puzzle, or None if there's no solution found.
        """
        for r in range(EVOLUTION_ROUND):
            evaluation = self._evaluate()
            if evaluation is not None:
                return evaluation
            print("evolution round {}, max adaptivity {}, individual {}".format(r, self.population[0].adaptivity,
                                                                                self.population[0]))
            self._select()
            self._crossover()
            self._mutate()
        return None

    def _evaluate(self) -> list[SolutionStep] | None:
        """
        Protected function, do not call directly.

        Evaluation is performed before evolution steps. Firstly, calculate the adaptivity of all individuals. Then
        sort the population according to the adaptivity descending-ly. If there's a solution, generate steps and return.

        :return: A list containing steps to solve the puzzle, or None if there's no solution found.
        """
        for individual in self.population:
            individual.calculate_adaptivity(self.initial, self.final)
        self.population.sort(reverse=True, key=lambda i: i.adaptivity)
        if self.population[0].adaptivity == FINAL_ADAPTIVITY:
            steps = []
            last_matrix = self.initial.clone()
            for gene in self.population[0].gene:
                current_matrix = last_matrix.play_only(gene)
                steps.append(SolutionStep(last_matrix, current_matrix))
                last_matrix = current_matrix
            return steps
        return None

    def _select(self) -> None:
        """
        Protected function, do not call directly.

        The select step of evolution. Firstly select two individuals from the population, repeat is allowed. Then
        compare those two individuals' adaptivity, the greater one will be put in the new population. This operation
        will repeat for `POPULATION_SIZE` times, in order to produce a new population with the same size as the old one.
        """
        new_population = []
        while len(new_population) < POPULATION_SIZE:
            a: Individual = random.choice(self.population)
            b: Individual = random.choice(self.population)
            new_population.append(a.clone() if a.adaptivity >= b.adaptivity else b.clone())
        self.population = new_population

    def _crossover(self) -> None:
        """
        Protected function, do not call directly.

        The crossover step of evolution. Select two non-repeat individuals from the population, and generate a
        possibility while iterating the genes. If the possibility is smaller than the `CROSSOVER_POSSIBILITY`,
        then perform the crossover of genes on the position between two individuals.
        """
        for _ in range(CROSSOVER_RANGE):
            a: Individual = random.choice(self.population)
            b: Individual = random.choice(self.population)
            while b is a:
                b = random.choice(self.population)
            for i in range(self.depth_limit):
                swap = True if random.random() < CROSSOVER_POSSIBILITY else False
                if swap:
                    a.gene[i], b.gene[i] = b.gene[i], a.gene[i]

    def _mutate(self) -> None:
        """
        Protected function, do not call directly.

        The mutate step of evolution. For an individual, select two different positions of the genes, and generate a
        possibility. If the possibility is smaller than `MUTATE_POSSIBILITY`, a swap operation is performed
        indicating a mutation.
        """
        for individual in self.population:
            mutate = True if random.random() < MUTATE_POSSIBILITY else False
            if mutate:
                pos_a = random.randrange(self.depth_limit)
                pos_b = random.randrange(self.depth_limit)
                while pos_b == pos_a:
                    pos_b = random.randrange(self.depth_limit)
                individual.gene[pos_a], individual.gene[pos_b] = individual.gene[pos_b], individual.gene[pos_a]
