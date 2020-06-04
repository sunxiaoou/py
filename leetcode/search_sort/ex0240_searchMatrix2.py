#! /usr/local/bin/python3
from bisect import bisect
from typing import List


def searchMatrix2(matrix: List[List[int]], target: int) -> bool:
    if not matrix or not matrix[0]:
       return False

    n = len(matrix)
    for i in range(n):
        j = bisect(matrix[i], target) - 1
        if matrix[i][j] == target:
            return True
    return False


def searchMatrix(matrix: List[List[int]], target: int) -> bool:
    if not matrix or not matrix[0]:
        return False

    n = len(matrix)
    i, j = 0, len(matrix[0]) - 1        # start from up-right conner
    while i < n and j >= 0:
        if matrix[i][j] == target:      # found the target
            return True
        if matrix[i][j] < target:       # is not in this row
            i += 1                      # try next row
        else:                           # is in this row or is not in matrix at all
            j -= 1                      # try previous column
    return False


def main():
    matrix = [[]]
    matrix = [[1,  3,  5,  7,  9],
              [2,  4,  6,  8,  10],
              [11, 13, 15, 17, 19],
              [12, 14, 16, 18, 20],
              [21, 22, 23, 24, 25]]

    matrix = [[1, 4, 7, 11, 15],
              [2, 5, 8, 12, 19],
              [3, 6, 9, 16, 22],
              [10, 13, 14, 17, 24],
              [18, 21, 23, 26, 30]]

    print(searchMatrix(matrix, 5))          # True
    print(searchMatrix(matrix, 17))         # True
    print(searchMatrix(matrix, 20))         # False


if __name__ == "__main__":
    main()
