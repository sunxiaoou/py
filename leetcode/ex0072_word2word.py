#! /usr/local/bin/python3
# https://leetcode-cn.com/problems/edit-distance/solution/edit-distance-by-ikaruga/
from typing import List


def print_grid(word1: str, word2: str, grid: List[List[int]]):
    print(['', ''] + [ch for ch in word1])
    w2 = [''] + list(word2)
    for i in range(len(w2)):
        print([w2[i]] + grid[i])


def minDistance(word1: str, word2: str) -> int:
    n1, n2 = len(word1), len(word2)

    if not word1 or not word2:
        return n1 + n2

    grid = [[0] * (n1 + 1) for _ in range(n2 + 1)]
    for j in range(n1 + 1):
        grid[0][j] = j
    for i in range(n2 + 1):
        grid[i][0] = i

    for i in range(1, n2 + 1):
        for j in range(1, n1 + 1):
            if word2[i - 1] != word1[j - 1]:
                grid[i][j] = min(grid[i - 1][j] + 1, grid[i][j - 1] + 1, grid[i - 1][j - 1] + 1)
            else:
                grid[i][j] = grid[i - 1][j - 1]
    print_grid(word1, word2, grid)
    return grid[i][j]


def main():
    print(minDistance("a", "aba"))              # 2
    print(minDistance("horse", "ros"))              # 3
    print(minDistance("intention", "execution"))    # 5
    print(minDistance("", ""))    # 0
    print(minDistance("mart", "karma"))    # 3


if __name__ == "__main__":
    main()
