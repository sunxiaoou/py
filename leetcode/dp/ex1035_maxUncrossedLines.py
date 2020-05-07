#! /usr/local/bin/python3
from typing import List


def create_grid(array1: List, array2: List) -> List[List]:
    grid = [[-1] + [n for n in array1]]
    for n in array2:
        # row = [n] + [0] * len(array1)
        # grid.append(row)
        grid.append([n] + [0] * len(array1))
    return grid


def print_grid(grid):
    for r in grid:
        for c in r:
            print(c, end="\t")
        print()
    print()


def maxUncrossedLines(A: List[int], B: List[int]) -> int:
    grid = create_grid(A, B)

    for i in range(1, len(grid)):
        for j in range(1, len(grid[0])):
            if grid[i][0] == grid[0][j]:    # a == b
                grid[i][j] = grid[i - 1][j - 1] + 1 if i > 1 and j > 1 else 1
            else:
                grid[i][j] = max(grid[i - 1][j] if i > 1 else 0, grid[i][j - 1] if j > 1 else 0)

    # print_grid(grid)
    return grid[i][j]


def main():
    print(maxUncrossedLines([1, 4, 2], [1, 2, 4]))     # 2
    print(maxUncrossedLines([2, 5, 1, 2, 5], [10, 5, 2, 1, 5, 2]))   # 3
    print(maxUncrossedLines([1, 3, 7, 1, 7, 5], [1, 9, 2, 5, 1]))    # 2


if __name__ == "__main__":
    main()
