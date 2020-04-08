#! /usr/local/bin/python3
from collections import deque
from typing import List


def print_grid(grid: List[List[int]]):
    print(' ', [i for i in range(len(grid[0]))])
    for i in range(len(grid)):
        print(i, grid[i])


# 1 <= n,m <= 100
# 0 <= k <= 20
def movingCount(m: int, n: int, k: int) -> int:
    grid = []
    for i in range(m):
        grid.append([1 if i // 10 + i % 10 + j // 10 + j % 10 > k else 0 for j in range(n)])
    # print_grid(grid)

    bfs = deque()
    grid[0][0] = 2
    bfs.append((0, 0))
    count = 0
    while bfs:
        i, j = bfs.popleft()
        # print('pop', i, j)
        count += 1
        if j < n - 1 and grid[i][j + 1] == 0:
            grid[i][j + 1] = 2
            bfs.append((i, j + 1))
        if i < m - 1 and grid[i + 1][j] == 0:
            grid[i + 1][j] = 2
            bfs.append((i + 1, j))
    # print_grid(grid)
    return count


def main():
    print(movingCount(2, 3, 1))     # 3
    print(movingCount(3, 1, 0))     # 1
    print(movingCount(3, 2, 17))
    print(movingCount(20, 20, 9))


if __name__ == "__main__":
    main()
