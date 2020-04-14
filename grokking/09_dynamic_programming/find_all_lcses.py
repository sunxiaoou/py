#! /usr/local/bin/python3
from typing import List


def print_grid(word1: str, word2: str, grid: List[List[int]]):
    print([' '] + [ch for ch in word1])
    for i in range(len(word2)):
        print([word2[i]] + grid[i])


def find_lcses(word1: str, word2: str) -> int:
    grid = [[0] * len(word1) for _ in word2]

    for i in range(len(word2)):
        for j in range(len(word1)):
            if word2[i] != word1[j]:
                grid[i][j] = max(grid[i - 1][j] if i > 0 else 0, grid[i][j - 1] if j > 0 else 0)
            else:
                grid[i][j] = grid[i - 1][j - 1] + 1 if i > 0 and j > 0 else 1
    lcs_len = grid[i][j]
    print_grid(word1, word2, grid)
    result = []

    def backtrack(lcs, i: int, j: int):
        if len(lcs) == lcs_len and (not result or result[-1] != [*lcs][:: -1]):
            result.append([*lcs][:: -1])
            return
        if word2[i] == word1[j]:
            lcs.append((i, j, word2[i]))
            backtrack(lcs, i - 1 if i > 0 else 0, j - 1 if j > 0 else 0)
            lcs.pop()
        else:
            if i > 0 and grid[i][j] == grid[i - 1][j]:
                backtrack(lcs, i - 1 if i > 0 else 0, j)
            if j > 0 and grid[i][j] == grid[i][j - 1]:
                backtrack(lcs, i, j - 1 if j > 0 else 0)

    backtrack([], len(word2) - 1, len(word1) - 1)
    print(result)

    return len(result)


def main():
    print(find_lcses("horse", "ros"))              # 2
    print(find_lcses("intention", "execution"))    # 2
    print(find_lcses("mart", "karma"))    # 2


if __name__ == "__main__":
    main()
