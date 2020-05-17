#! /usr/local/bin/python3
from typing import List


def setZeroes(matrix: List[List[int]]) -> None:
    n, m = len(matrix), len(matrix[0])
    pos = [(i, j) for j in range(m) for i in range(n) if not matrix[i][j]]

    for i, j in pos:
        for k in range(n):
            matrix[k][j] = 0
        for k in range(m):
            matrix[i][k] = 0

    for i in matrix:
        print(i)


def main():
    matrix = [[1, 1, 1],            # [1 ,0, 1]
              [1, 0, 1],            # [0, 0, 0]
              [1, 1, 1]]            # [1 ,0, 1]
    setZeroes(matrix)

    matrix = [[0, 1, 2, 0],         # [0, 0, 0, 0]
              [3, 4, 5, 2],         # [0, 4, 5, 0]
              [1, 3, 1, 5]]         # [0, 3, 1, 0]
    setZeroes(matrix)


if __name__ == "__main__":
    main()
