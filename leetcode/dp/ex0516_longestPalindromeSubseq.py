#! /usr/local/bin/python3
from typing import List


def print_grid(word1: str, word2: str, grid: List[List[int]]):
    print([' '] + [ch for ch in word1])
    for i in range(len(word2)):
        print([word2[i]] + grid[i])


def find_lcs(word1: str, word2: str) -> int:
    grid = [[0] * len(word1) for _ in word2]

    for i in range(len(word2)):
        for j in range(len(word1)):
            if word2[i] != word1[j]:
                grid[i][j] = max(grid[i - 1][j] if i > 0 else 0, grid[i][j - 1] if j > 0 else 0)
            else:
                grid[i][j] = grid[i - 1][j - 1] + 1 if i > 0 and j > 0 else 1
    print_grid(word1, word2, grid)
    return grid[i][j]


def longestPalindromeSubseq(s: str) -> int:
    return find_lcs(s, s[:: -1])


def main():
    print(longestPalindromeSubseq("bbbab"))     # 4
    print(longestPalindromeSubseq("cbbd"))      # 2


if __name__ == "__main__":
    main()
