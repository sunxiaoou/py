#! /usr/local/bin/python3
from typing import List

"""
dp[i][j] represents side length of the max square, whose down-right conner is at (i, j).
then
dp [i][j] = min(dp[i - 1][j], dp[i - 1][j - 1], dp[i][j - 1]) + 1
it means current square area depends on 3 previous squares (up, left, and up-left), for example:
    1 1 1 1 0       # given (i, j) is (3, 4)
    1 1 1 1 1       # then dp[i - 1, j] is dp[2][4] = 2
    1 1 1 1 1       # dp[i - 1][j - 1] is dp[2][3] = 3 and dp[i][j - 1] is dp[3, 3] = 1 
    0 0 0 1 1       # so dp[i][j] = min(2, 3, 1) + 1 = 2
"""


def print_dp(row: List[int], col: List[int], dp: List[List[int]]):
    row0 = ['\\\\'] + [str(i) for i in row]
    print(', '.join(row0))
    for i in range(len(col)):
        print("{},  {}".format(str(col[i]),
                               ', '.join([str(j) if str(j) != 'inf' else '∞' for j in dp[i]])))


def maximalSquare(matrix: List[List[str]]) -> int:
    if not matrix:
        return 0
    m, n = len(matrix), len(matrix[0])
    dp = [[0] * n for _ in range(m)]
    for i in range(m):
        dp[i][0] = 0 if matrix[i][0] == '0' else 1
    for j in range(n):
        dp[0][j] = 0 if matrix[0][j] == '0' else 1
    # print_dp([i for i in range(n)], [j for j in range(m)], dp)
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == '0':
                dp[i][j] = 0
            else:
                dp[i][j] = min(dp[i - 1][j], dp[i - 1][j - 1], dp[i][j - 1]) + 1
    # print_dp([i for i in range(n)], [j for j in range(m)], dp)
    side = max(max(i) for i in dp)
    return side * side


def main():
    matrix = [["1", "0", "1", "0", "0"],
              ["1", "0", "1", "1", "1"],
              ["1", "1", "1", "1", "1"],
              ["1", "0", "0", "1", "0"]]
    print(maximalSquare(matrix))            # 4
    matrix = [["0", "1", "1", "0", "0", "1", "0", "1", "0", "1"],
              ["0", "0", "1", "0", "1", "0", "1", "0", "1", "0"],
              ["1", "0", "0", "0", "0", "1", "0", "1", "1", "0"],
              ["0", "1", "1", "1", "1", "1", "1", "0", "1", "0"],
              ["0", "0", "1", "1", "1", "1", "1", "1", "1", "0"],
              ["1", "1", "0", "1", "0", "1", "1", "1", "1", "0"],
              ["0", "0", "0", "1", "1", "0", "0", "0", "1", "0"],
              ["1", "1", "0", "1", "1", "0", "0", "1", "1", "1"],
              ["0", "1", "0", "1", "1", "0", "1", "0", "1", "1"]]
    print(maximalSquare(matrix))            # 4
    print(maximalSquare([["0"]]))           # 0
    print(maximalSquare([["1"]]))           # 1


if __name__ == "__main__":
    main()
