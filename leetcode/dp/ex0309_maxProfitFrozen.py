#! /usr/local/bin/python3
from typing import List


def maxProfit(prices: List[int]) -> int:
    n = len(prices)
    if n < 2:
        return 0
    dp = [[0] * n for _ in range(2)]
    dp[0][0] = 0
    dp[1][0] = -prices[0]
    for i in range(1, n):
        dp[0][i] = max(dp[0][i - 1], dp[1][i - 1] + prices[i])
        dp[1][i] = max(dp[1][i - 1], dp[0][i - 2] - prices[i])
    print(dp[0])
    print(dp[1])
    return dp[0][-1]


def main():
    print(maxProfit([1, 2, 3, 0, 2]))       # 3
    print(maxProfit([1, 2, 0, 3, 2]))       # 3
    print(maxProfit([1, 2, 3, 4, 5]))       # 4
    print(maxProfit([1]))                   # 0
    print(maxProfit([7, 1, 5, 3, 6, 4]))    # 5
    print(maxProfit([7, 6, 4, 3, 1]))       # 0


if __name__ == "__main__":
    main()
