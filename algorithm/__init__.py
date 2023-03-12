"""
Author: Cylix Lee (cylix.lee@foxmail.com).
Created on: March 11th, 2023

A module containing all implemented algorithms to solve the puzzle.
"""
from __future__ import annotations

import matrix
from util import UnimplementedException


def differentiate(old: matrix.Matrix, new: matrix.Matrix) -> set[int]:
    """
    Collect elements with different positions in those two matrices.

    :param old: One matrix to be checked.
    :param new: Another matrix to be checked.
    :return: A set containing those differently-positioned elements.
    """
    difference = set()
    for i in range(3):
        for j in range(3):
            old_number = old.fetch(i, j)
            new_number = new.fetch(i, j)
            if old_number != new_number:
                difference.add(old_number)
                difference.add(new_number)
    return difference


class InvalidStepException(Exception):
    """
    An exception class representing that it's impossible to turn an arrangement into another within 1 step.
    """

    def __init__(self, old: matrix.Matrix, new: matrix.Matrix) -> None:
        super().__init__("cannot turn {} to {} in one step".format(old, new))


class SolutionStep:
    """
    A class describing one of the steps to solve the puzzle. Note that str(self) will generate a human-readable
    instruction describing this step.
    """

    def __init__(self, old: matrix.Matrix, new: matrix.Matrix) -> None:
        """
        Analyze the difference between two matrices, and generate a step to turn the old matrix into the new one.
        """
        difference = differentiate(old, new)
        if len(difference) != 2:
            raise InvalidStepException(old, new)
        if matrix.SPACE_VALUE not in difference:
            raise InvalidStepException(old, new)
        for d in difference:
            if d != matrix.SPACE_VALUE:
                self.click = d
                break
        self.target = new.clone()

    def __str__(self) -> str:
        return "click {}, and the matrix should be {}".format(self.click, self.target)


class SolutionAlgorithm:
    """
    A base class, or called `interface`, of all solution-algorithm implementations.
    """

    def __init__(self, initial_matrix: matrix.Matrix, final_matrix: matrix.Matrix) -> None:
        self.initial = initial_matrix.clone()
        self.final = final_matrix.clone()

    def __str__(self) -> str:
        raise UnimplementedException()

    def solve(self) -> list[SolutionStep] | None:
        """
        Solve the puzzle whose initial and final arrangements are specified in constructor.

        :return: A list containing steps to solve the puzzle, or None if there's no solution found.
        """
        raise UnimplementedException()
