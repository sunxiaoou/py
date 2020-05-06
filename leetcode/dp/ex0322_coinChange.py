#! /usr/local/bin/python3
from typing import List


def print_dp(dp: List[List[int]]):
    n1, n2 = len(dp), len(dp[0])
    row0 = ['\\\\'] + [str(i) for i in range(n2)]
    print(', '.join(row0))
    for i in range(n1):
        print("{},  {}".format(i, ', '.join([str(j) for j in dp[i]])))


def coinChange(coins: List[int], amount: int) -> int:
    m, n = len(coins), amount + 1
    dp = [[0] * n for _ in coins]
    for i in range(n):
        q, r = divmod(i, coins[0])
        dp[0][i] = q if r == 0 else float('inf')

    for i in range(1, m):
        for j in range(1, n):
            if j < coins[i]:
                dp[i][j] = dp[i - 1][j]
            else:           # this is a unbounded knapsack problem
                dp[i][j] = min(dp[i - 1][j], dp[i][j - coins[i]] + 1)

    print_dp(dp)
    return dp[-1][-1] if dp[-1][-1] != float('inf') else -1


def main():
    print(coinChange([1, 2, 5], 11))            # 3
    """
    \\, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
    0,  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
    1,  0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6
    2,  0, 1, 1, 2, 2, 1, 2, 2, 3, 3, 2, 3
    3
    """
    print(coinChange([2], 3))                   # -1
    """
    \\, 0, 1, 2, 3
    0,  0, inf, 1, inf
    -1
    """


if __name__ == "__main__":
    main()
