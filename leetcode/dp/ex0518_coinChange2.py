#! /usr/local/bin/python3
from typing import List


# dp[i][j] = dp[i - 1][j] + dp[i][j - coins[i]]
# i: index of current coin
# j: current amount
# dp[i][j]: current total ways number, it is consist of 2 parts:
# 1) dp[i - 1][j]: total ways without current coin
# 2) dp[i][j - coins[i]]: ways for (current amount - one current coin value)
# 2nd part means ways number doesn't increase if only considering current coin
# so you can use previous ways number as well
def waysToChange(amount: int, coins: List[int]) -> int:
    m, n = amount + 1, len(coins)
    if not n:
        return 1 if m == 1 else 0
    dp = [[0] * m for _ in range(n)]
    for j in range(m):                  # set first line
        dp[0][j] = 0 if j % coins[0] else 1
    # print(dp[0])
    for i in range(1, n):
        for j in range(m):
            if j < coins[i]:            # current coin is useless
                dp[i][j] = dp[i - 1][j]
            else:
                dp[i][j] = dp[i - 1][j] + dp[i][j - coins[i]]
        # print(dp[i])
    return dp[-1][-1] % 1000000007


def main():
    print(waysToChange(0, []))                      # 1
    print(waysToChange(5, [1, 2, 5]))               # 4
    """
       0, 1, 2, 3, 4, 5
    1  1, 1, 1, 1, 1, 1
    2  1, 1, 2, 2, 3, 3   
    3  1, 1, 2, 2, 3, 4
    """
    print(waysToChange(3, [2]))                     # 0
    print(waysToChange(10, [10]))                   # 1
    print(waysToChange(26, [25, 10, 5, 1]))         # 13
    print(waysToChange(900750, [25, 10, 5, 1]))     # 504188296


if __name__ == "__main__":
    main()
