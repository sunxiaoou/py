#! /usr/local/bin/python3
from collections import deque
from typing import List


def maxDistance_slow(grid: List[List[int]]) -> int:
    if not grid:
        return -1

    seas = []
    lands = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                seas.append((i, j))
            else:
                lands.append((i, j))

    if not seas or not lands:
        return -1

    # return max(min(abs(sea[0] - land[0]) + abs(sea[1] - land[1]) for land in lands) for sea in seas)
    max_min = 0
    for sea in seas:
        minimum = float('inf')
        for land in lands:
            distance = abs(sea[0] - land[0]) + abs(sea[1] - land[1])
            if max_min > 0 and distance <= max_min:
                break
            if distance < minimum:
                minimum = distance
        else:
            max_min = max(max_min, minimum)

    return max_min


def maxDistance(grid: List[List[int]]) -> int:
    n = len(grid)
    bfs = deque()
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1:
                bfs.append((i, j, 0))

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    level = 0
    while bfs:
        land = bfs.popleft()
        level = max(level, land[2])
        for di in directions:
            i = land[0] + di[0]
            j = land[1] + di[1]
            if 0 <= i < n and 0 <= j < n and grid[i][j] == 0:
                bfs.append((i, j, land[2] + 1))
                grid[i][j] = 1
    return -1 if level == 0 else level


def main():
    print(maxDistance([[1, 0, 1],[0, 0, 0],[1, 0, 1]]))
    print(maxDistance([[1, 0, 0],[0, 0, 0],[0, 0, 0]]))
    print(maxDistance([]))


if __name__ == "__main__":
    main()
