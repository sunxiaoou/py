#! /usr/local/bin/python3
from typing import List


def uniquePathsWithObstacles(obstacleGrid: List[List[int]]) -> int:
    if obstacleGrid[0][0]:
        return 0
    m, n = len(obstacleGrid), len(obstacleGrid[0])
    dp = obstacleGrid
    blocked = False
    for i in range(m):
        if blocked:
            dp[i][0] = 0
        elif dp[i][0]:
            dp[i][0] = 0
            blocked = True
        else:
            dp[i][0] = 1
    blocked = False
    for j in range(1, n):
        if blocked:
            dp[0][j] = 0
        elif dp[0][j]:
            dp[0][j] = 0
            blocked = True
        else:
            dp[0][j] = 1
    # for i in dp:
    #     print(i)
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = 0 if dp[i][j] else dp[i - 1][j] + dp[i][j - 1]
    # for i in dp:
    #    print(i)
    return dp[-1][-1]


def main():
    print(uniquePathsWithObstacles([[0, 0], [1, 1], [0, 0]]))               # 2
    print(uniquePathsWithObstacles([[1, 0]]))      # 2
    print(uniquePathsWithObstacles([[0, 0, 0], [0, 1, 0], [0, 0, 0]]))      # 2



if __name__ == "__main__":
    main()
