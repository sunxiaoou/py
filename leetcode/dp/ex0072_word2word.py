#! /usr/local/bin/python3
# https://leetcode-cn.com/problems/edit-distance/solution/edit-distance-by-ikaruga/
from typing import List


"""
delete:     grid[i][j - 1] + 1 to grid[i][j]
add:        grid[i - 1][j] + 1 to grid[i][j]
change:     grid[i - 1][j - 1] + 1 to grid[i][j]

mart -> karma
1)
\, '', m, a, r, t
'',  0, 1, 2, 3, 4          # first row: 'mart' -> '', delete m, a, r, t continually, ops = 1, 2, 3, 4  
k,  1, 1, 2, 3, 4           #  m -> k, ma -> k, mar -> k, mart ->, ops = 1, 2, 3, 4 
a,  2, 0, 0, 0, 0
r,  3, 0, 0, 0, 0
m,  4, 0, 0, 0, 0
a,  5, 0, 0, 0, 0           # first column: '' -> 'karma, add k, a , r , m, a continually,  ops = 1, 2, 3, 4, 5

2)
\, '', m, a, r, t
'',  0, 1, 2, 3, 4
k,  1, 1, 2, 3, 4           
a,  2, 2, 1, 2, 3           # m -> ka, ma -> ka, mar -> ka, mart -> ka, ops = 2, 1, 2, 3
r,  3, 0, 0, 0, 0
m,  4, 0, 0, 0, 0
a,  5, 0, 0, 0, 0

"""


def print_grid(word1: str, word2: str, grid: List[List[int]]):
    row0 = ['\\', '\'\''] + [ch for ch in word1]
    print(', '.join(row0))
    w2 = ['\'\''] + list(word2)
    for i in range(len(w2)):
        print("{},  {}".format(w2[i], ', '.join([str(j) for j in grid[i]])))


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
