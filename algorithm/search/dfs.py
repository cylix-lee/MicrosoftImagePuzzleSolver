"""
Author: Cylix Lee (cylix.lee@foxmail.com).
Created on: March 12th, 2023

Depth-First Search algorithm to solve the puzzle.
"""
from __future__ import annotations

import matrix
from algorithm import SolutionAlgorithm, SolutionStep


class DepthFirstSearch(SolutionAlgorithm):
    """
    The DFS algorithm class that performs depth-first search with a depth limit. Compared to BFS, this algorithm
    doesn't ensure that there's a solution within given steps. The solution, if any, may not be the optimal one either.

    However, if lucky, this algorithm may take a much shorter time than BFS.
    """

    def __init__(self, depth_limit: int, initial_matrix: matrix.Matrix, final_matrix: matrix.Matrix) -> None:
        super().__init__(initial_matrix, final_matrix)
        self.depth_limit = depth_limit

    def __str__(self) -> str:
        return "depth-limited Depth-First Search (depth_limit={})".format(self.depth_limit)

    def solve(self) -> list[SolutionStep]:
        return self._dfs(1, self.initial)

    def _dfs(self, depth: int, target: matrix.Matrix) -> list[SolutionStep] | None:
        """
        Protected function, do not call directly. DFS algorithms are often implemented through a recurrence form.

        :param depth: Current depth. If the depth is bigger than the depth limit given in constructor, this function
            will immediately return.
        :param target: The matrix to work on.
        :return: A list containing the solving steps, or None if there's no solution within given depth limit.
        """
        if depth > self.depth_limit:
            return None
        parents = target.parents()
        children = [candidate for candidate in target.play() if candidate not in parents]
        for child in children:
            if child == self.final:
                iterator = child
                steps = []
                while iterator.parent is not None:
                    steps.append(SolutionStep(iterator.parent, iterator))
                    iterator = iterator.parent
                return steps[::-1]
            child_dfs = self._dfs(depth + 1, child)
            if child_dfs is not None:
                return child_dfs
        return None
