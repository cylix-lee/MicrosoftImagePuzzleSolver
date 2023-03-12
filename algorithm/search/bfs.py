"""
Author: Cylix Lee (cylix.lee@foxmail.com).
Created on: March 11th, 2023

Breadth-First Search algorithm to solve the puzzle.
"""
from __future__ import annotations

import queue

import matrix
from algorithm import SolutionAlgorithm, SolutionStep


class BreadthFirstSearch(SolutionAlgorithm):
    """
    The BFS algorithm class that performs search without depth limit. Theoretically, this algorithm returns the
    optimal solution, if any.

    Note that this algorithm may cause extremely long time to solve the puzzle.
    """

    def __str__(self) -> str:
        return "Breadth-First Search"

    def solve(self) -> list[SolutionStep] | None:
        matrix_queue = queue.Queue()
        matrix_queue.put(self.initial)
        while matrix_queue.qsize() > 0:
            target: matrix.Matrix = matrix_queue.get()
            if target == self.final:
                steps = []
                while target.parent is not None:
                    steps.append(SolutionStep(target.parent, target))
                    target = target.parent
                return steps[::-1]
            for new_target in target.play():
                if new_target not in target.parents():
                    matrix_queue.put(new_target)
