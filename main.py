import algorithm.search
import algorithm.heuristic
import matrix

USAGE = """Welcome to Microsoft Image Puzzle Solver!
Please input a {}x{} matrix as the initial arrangement, and leave a '#' where the space lays.
For example:
  123
  4{}5
  678
And input the targeted arrangement in the same format of the former one.""".format(matrix.MATRIX_SIZE,
                                                                                   matrix.MATRIX_SIZE,
                                                                                   matrix.SPACE_SYMBOL)

if __name__ == "__main__":
    print(USAGE)
    initial = matrix.Matrix([input() for _ in range(matrix.MATRIX_SIZE)])
    print("Initial matrix {} confirmed. Please input final matrix: ".format(initial))
    final = matrix.Matrix([input() for _ in range(matrix.MATRIX_SIZE)])
    print("Final matrix {} confirmed. Please input index of the algorithm to use:".format(final))
    print(" 1. BFS (Breadth-First Search) [Default]")
    print(" 2. depth-limited DFS (Depth-First Search)")
    print(" 3. depth-limited Genetic Algorithm (Heuristic)")

    alg_index = input()
    try:
        alg_index = int(alg_index)
    except ValueError:
        alg_index = 1

    alg = algorithm.search.BreadthFirstSearch(initial, final)
    if alg_index == 2:
        print("depth-limited DFS needs a depth limit, please input:")
        alg = algorithm.search.DepthFirstSearch(int(input()), initial, final)
    elif alg_index == 3:
        print("depth-limited Genetic Algorithm needs a depth limit, please input:")
        alg = algorithm.heuristic.GeneticAlgorithm(int(input()), initial, final)

    print("Solving the puzzle with {}...".format(alg))
    solution = alg.solve()
    if solution is None:
        print("No solution found using {}, sorry.".format(alg))
    else:
        print("Solution found, with {} steps in total. Please follow the steps below:".format(len(solution)))
        for step in solution:
            print(" {}".format(step))
        print("Have a nice game!")
