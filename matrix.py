"""
Author: Cylix Lee (cylix.lee@foxmail.com).
Created on: March 10th, 2023

Classes that help representing the 3x3 arrangement, both initial and final. The arrangements are able to fetch/place
(get/set the number on certain position), clone, and to produce new matrices based on moving the space tile along 4
directions or fewer.

"""
from __future__ import annotations

import copy
import enum

import util

MATRIX_SIZE = 3
SPACE_SYMBOL = "#"
SPACE_VALUE = -1


def boundary_check(candidates: list[int]) -> bool:
    """
    Simple function to check if the candidates are valid since the matrix size is given.

    :param candidates: a list of numbers need to be checked.
    :return: True if those numbers are valid as the index of a matrix, otherwise False.
    """
    for candidate in candidates:
        if not (0 <= candidate < MATRIX_SIZE):
            return False
    return True


class Direction(enum.Enum):
    """
    An enum class representing directions the space tile can move towards.
    """
    LEFT = (0, -1)
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)


DIRECTIONS = [
    Direction.LEFT,
    Direction.UP,
    Direction.RIGHT,
    Direction.DOWN,
]


class Matrix:
    """
    A class representing the arrangement of puzzle, whose inner data structure is a two-dimensional list. This class
    provides useful operations, since operating the list is not recommended and may lead to unexpected behaviours.
    """

    def __init__(self, data: list[str] = None) -> None:
        """
        Create a Matrix instance to represent the initial or final status of the puzzle. Note that if data is not
        None, then it must be well-formed.

        :param data: Optional, a list containing 3 str, with 3 letters each.
        """
        self._arrangement = [[SPACE_VALUE for _ in range(MATRIX_SIZE)] for _ in range(MATRIX_SIZE)]
        self._space_position = None
        self.parent = None
        self.last_direction = None
        if data is None:
            return
        spaced = False
        appeared = {number: False for number in range(1, MATRIX_SIZE * MATRIX_SIZE)}
        for line_index, line in enumerate(data):
            if not boundary_check([line_index]):
                util.fatal("too many lines. {} expected.".format(MATRIX_SIZE))
            line = line.strip()
            if len(line) != MATRIX_SIZE:
                util.fatal("invalid matrix format. expected {} elements per line, got {}".format(
                    MATRIX_SIZE, len(line)))
            for char_index, char in enumerate(line):
                if char == SPACE_SYMBOL:
                    if spaced:
                        util.fatal("multiple spaces are unacceptable")
                    self.place(line_index, char_index, SPACE_VALUE)
                    spaced = True
                    continue
                number = int(char)
                if appeared[number]:
                    util.fatal("repeated number {} founded".format(number))
                appeared[number] = True
                self.place(line_index, char_index, number)

    def __str__(self) -> str:
        return "Matrix({})".format(str(self._arrangement))

    def __eq__(self, other: Matrix) -> bool:
        return self._arrangement == other._arrangement

    def parents(self) -> list[Matrix]:
        """
        Get all parents of self. Often used along with keyword `in`.

        :return: A list containing all parents of self.
        """
        iterator = self
        result = []
        while iterator.parent is not None:
            result.append(iterator.parent)
            iterator = iterator.parent
        return result

    def clone(self) -> Matrix:
        """
        Clone this Matrix instance. The new instance has the same data with the original one, but is independent in
        memory.

        :return: A new Matrix instance with its memory independent of the original one.
        """
        mat = Matrix()
        mat._arrangement = copy.deepcopy(self._arrangement)
        mat._space_position = copy.deepcopy(self._space_position)
        return mat

    def place(self, row: int, column: int, number: int) -> None:
        """
        Place a certain number in the position (row, column) of Matrix.
        """
        if not boundary_check([row, column]):
            util.fatal("cannot place number {} at an invalid position ({}, {})".format(
                number, row, column))
        if number == SPACE_VALUE:
            self._space_position = (row, column)
        self._arrangement[row][column] = number

    def fetch(self, row: int, column: int) -> int:
        """
        Return the number in the position (row, column) of Matrix.
        """
        if not boundary_check([row, column]):
            util.fatal("cannot fetch number at an invalid position ({}, {})".format(
                row, column))
        return self._arrangement[row][column]

    def exchange(self, x1: int, y1: int, x2: int, y2: int) -> None:
        """
        Exchange the numbers on the position (x1, y1) and (x2, y2).
        """
        if not boundary_check([x1, x2, y1, y2]):
            return
        temp = self.fetch(x1, y1)
        self.place(x1, y1, self.fetch(x2, y2))
        self.place(x2, y2, temp)

    def play(self, forbidden_directions: list[Direction] = None) -> list[Matrix]:
        """
        Generate new arrangements through moving the space tile around. The function ensures that space tile will not
        move out of the boundary, and will not move towards the directions forbidden.

        :param forbidden_directions: A list containing directions the space tile is forbidden to move towards
        :return: A list containing new matrices, if any, with different arrangements by moving the space tile.
        """
        new_matrices = []
        space_x, space_y = self._space_position
        for direction in Direction:
            if forbidden_directions is not None and direction in forbidden_directions:
                continue
            delta_x, delta_y = direction.value
            x, y = space_x + delta_x, space_y + delta_y
            if not boundary_check([x, y]):
                continue
            mat = self.clone()
            mat.exchange(space_x, space_y, x, y)
            mat.parent = self
            mat.last_direction = direction
            new_matrices.append(mat)
        return new_matrices

    def play_towards(self, towards_directions: list[Direction]) -> list[Matrix]:
        """
        Generate new arrangements through moving the space tile towards specified directions. When the space is
        moving out of boundary towards a certain direction given, the matrix of this moving will not be returned.
        That's to say, the return value may still be an empty list.


        :param towards_directions: Directions to move the space tile.
        :return: A list containing new matrices generated through moving the space towards specified directions.
        """
        new_matrices = []
        space_x, space_y = self._space_position
        for direction in towards_directions:
            delta_x, delta_y = direction.value
            x, y = space_x + delta_x, space_y + delta_y
            if not boundary_check([x, y]):
                continue
            mat = self.clone()
            mat.exchange(space_x, space_y, x, y)
            mat.parent = self
            mat.last_direction = direction
            new_matrices.append(mat)
        return new_matrices

    def play_only(self, direction: Direction) -> Matrix | None:
        """
        Generate a new arrangement through moving the space tile towards the specified direction. Note that if the
        space tile is moved out of boundary, this matrix will not be returned.

        :param direction: The only direction to move the space tile towards.
        :return: A new matrix through moving the space tile towards given direction, or None if the space tile is out
            of boundary.
        """
        space_x, space_y = self._space_position
        delta_x, delta_y = direction.value
        x, y = space_x + delta_x, space_y + delta_y
        if not boundary_check([x, y]):
            return None
        mat = self.clone()
        mat.exchange(space_x, space_y, x, y)
        mat.parent = self
        mat.last_direction = direction
        return mat
