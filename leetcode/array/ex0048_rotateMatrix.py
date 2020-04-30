#! /usr/local/bin/python3
from typing import List


def rotate2(matrix: List[List[int]]) -> None:
    n = len(matrix)
    for k in range(n // 2):     # k represents circle, 0 is the outermost
        # for each circle, length = n - k, only needs to traversal m(k, k) ... m(k, n - k - 1)
        for j in range(k, n - k - 1):
            # 4 steps:  up -> right -> down -> left -> up
            # for each step:  m(i, j) -> m(j, n - 1 - i)
            x, matrix[j][n - k - 1] = matrix[j][n - k - 1], matrix[k][j]        # up -> right
            x, matrix[n - k - 1][n - j - 1] = matrix[n - k - 1][n - j - 1], x   # right -> down
            x, matrix[n - j - 1][k] = matrix[n - j - 1][k], x                   # down -> left
            matrix[k][j] = x                                                    # left -> up
        # for i in matrix:
        #     print(i)


def rotate(matrix: List[List[int]]) -> None:
    n = len(matrix)
    for i in range(n):                  # firstly swap up_right and down_left
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for i in range(n // 2):             # secondly swap left and right
        for j in range(n):
            matrix[j][i], matrix[j][n - 1 - i] = matrix[j][n - 1 - i], matrix[j][i]
    # for i in matrix:
    #    print(i)


def main():
    matrix = [[1, 2],
              [3, 4]]
    answer = [[3, 1],
              [4, 2]]
    rotate(matrix)
    print('OK') if matrix == answer else print('KO')

    matrix = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]]
    answer = [[7, 4, 1],
              [8, 5, 2],
              [9, 6, 3]]
    rotate(matrix)
    print('OK') if matrix == answer else print('KO')

    matrix = [[5, 1, 9, 11],
              [2, 4, 8, 10],
              [13, 3, 6, 7],
              [15, 14, 12, 16]]
    answer = [[15, 13, 2, 5],
              [14, 3, 4, 1],
              [12, 6, 8, 9],
              [16, 7, 10, 11]]
    rotate(matrix)
    print('OK') if matrix == answer else print('KO')


if __name__ == "__main__":
    main()
