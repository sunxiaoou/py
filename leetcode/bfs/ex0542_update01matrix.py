#! /usr/local/bin/python3
from collections import deque
from typing import List


def print_matrix(matrix: List[List[int]]):
    for i in matrix:
        print(i)


def updateMatrix(matrix: List[List[int]]) -> List[List[int]]:
    n1, n2 = len(matrix), len(matrix[0])

    flags = [[0] * n2 for _ in range(n1)]           # note: cannot use [[0] * n2] * n1

    bfs = deque()
    for i in range(n1):                             # add all matrix[i][j] == 0 to queue
        for j in range(n2):
            if not matrix[i][j]:
                bfs.append((i, j))
                flags[i][j] = 1

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]     # up, down, left, right
    while bfs:
        i0, j0 = bfs.popleft()
        for di, dj in directions:
            i, j = i0 + di, j0 + dj
            if 0 <= i < n1 and 0 <= j < n2 and not flags[i][j]:
                matrix[i][j] = matrix[i0][j0] + 1       # increase level
                bfs.append((i, j))
                flags[i][j] = 1

    return matrix


def main():
    m = [[0, 0, 0],
         [0, 1, 0],
         [1, 1, 1]]
    print_matrix(updateMatrix(m))
    m = [[0, 0, 0],
         [0, 1, 0],
         [0, 0, 0]]
    print_matrix(updateMatrix(m))


if __name__ == "__main__":
    main()
