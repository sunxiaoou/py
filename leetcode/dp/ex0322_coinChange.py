#! /usr/local/bin/python3
from typing import List


def print_dp(dp: List[List[int]]):
    n1, n2 = len(dp), len(dp[0])
    row0 = ['\\\\'] + [str(i) for i in range(n2)]
    print(', '.join(row0))
    for i in range(n1):
        print("{},  {}".format(i, ', '.join([str(j) for j in dp[i]])))


def coinChange(coins: List[int], amount: int) -> int:
    m, n = amount + 1, len(coins)           # add extra 0 for amount 0
    dp = [[0] * m for _ in range(n)]        # first 0 represents 0 coin combines amount 0
    for j in range(m):                      # set first dp[i - 1] for subsequent dp[i]
        qu, re = divmod(j, coins[0])
        dp[0][j] = qu if re == 0 else float('inf')  # inf represents can't combine the amount

    for i in range(1, n):
        for j in range(1, m):
            if j < coins[i]:
                dp[i][j] = dp[i - 1][j]
            else:           # this is a unbounded knapsack problem
                dp[i][j] = min(dp[i - 1][j], dp[i][j - coins[i]] + 1)
                # dp[i][j - coins[i]] can be inf, but float('inf ') + 1 == float('inf)

    # print_dp(dp)
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
