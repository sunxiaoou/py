#! /usr/local/bin/python3
from typing import List


def print_grid(word1: str, word2: str, grid: List[List[int]]):
    print([' '] + [ch for ch in word1])
    for i in range(len(word2)):
        print([word2[i]] + grid[i])


def minDistance(word1: str, word2: str) -> int:
    if not word1 or not word2:
        return max(len(word1), len(word2))

    grid = [[0] * len(word1)] * len(word2)      # word1 is first row, word2 is first column
    print_grid(word1, word2, grid)

    """
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if word2[i] != word1[j]:
                grid[i][j] = max(grid[i - 1][j] if i > 0 else 0, grid[i][j - 1] if j > 0 else 0)
            else:
                grid[i][j] = grid[i - 1][j - 1] + 1 if i > 0 and j > 0 else 1
    print_grid(word1, word2, grid)
    """
    grid = [[0] * len(word1) for _ in word2]
    print_grid(word1, word2, grid)

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if word2[i] != word1[j]:
                grid[i][j] = max(grid[i - 1][j] if i > 0 else 0, grid[i][j - 1] if j > 0 else 0)
            else:
                grid[i][j] = grid[i - 1][j - 1] + 1 if i > 0 and j > 0 else 1
    print_grid(word1, word2, grid)


    lcs = []
    while True:
        if word2[i] == word1[j]:
            lcs.append((i, j, word2[i]))
            if i > 0 and j > 0:
                i, j = i - 1, j - 1
            else:
                break
        else:
            if j > 0 and grid[i][j] == grid[i][j - 1]:
                j = j - 1
            elif i > 0 and grid[i][j] == grid[i - 1][j]:
                i = i - 1
            else:
                break
    lcs = lcs[:: -1]
    print(lcs)
    count, i0, j0 = 0, 0, 0
    for i, j, _ in lcs:
        count += max(len(word2[i0: i]), len(word1[j0: j]))
        print('{}, {}, {}'.format(word2[i0: i], word1[j0: j], count))
        i0, j0 = i + 1, j + 1
    count += max(len(word2[i0:]), len(word1[j0:]))
    print('{}, {}, {}'.format(word2[i0:], word1[j0:], count))

    return count


def main():
    print(minDistance("horse", "ros"))              # 3
    print(minDistance("intention", "execution"))    # 5
    # print(minDistance("", ""))    # 5
    print(minDistance("mart", "karma"))    # 3



if __name__ == "__main__":
    main()
