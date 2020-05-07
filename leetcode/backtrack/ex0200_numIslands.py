#! /usr/local/bin/python3
from typing import List


def print_grid(grid: List[List]):
    for i in range(len(grid)):
        print(grid[i])


def numIslands(grid: List[List[str]]) -> int:
    if not grid:
        return 0

    n1, n2 = len(grid), len(grid[0])
    flags = [[0] * n2 for _ in range(n1)]   # 0: not marked, 1: marked

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def backtrack(i: int, j: int):          # mark whole island since current land point
        flags[i][j] = 1                     # marked land point
        for x, y in directions:             # try to move up, down, left, right
            i1 = i + y if 0 <= i + y < n1 else i
            j1 = j + x if 0 <= j + x < n2 else j
            if grid[i1][j1] == '1' and flags[i1][j1] == 0:
                backtrack(i1, j1)           # search next point recursively

    count = 0
    for i in range(n1):
        for j in range(n2):                 # search all no marked points
            if grid[i][j] == '1' and flags[i][j] == 0:
                count += 1
                backtrack(i, j)
                # print_grid(flags)
                # print()
    return count


def main():
    print(numIslands([['0']]))              # 0
    grid = [["1", "0", "1", "1", "0", "1", "1"]]
    print(numIslands(grid))                 # 3
    grid = [["1", "1", "0", "0", "0"],
            ["1", "1", "0", "0", "0"],
            ["0", "0", "1", "0", "0"],
            ["0", "0", "0", "1", "1"]]
    print(numIslands(grid))                 # 3
    grid = [["1", "1", "1", "1", "0"],
            ["1", "1", "0", "0", "0"],
            ["1", "1", "0", "0", "0"],
            ["0", "0", "0", "0", "0"]]
    print(numIslands(grid))                 # 1


if __name__ == "__main__":
    main()
