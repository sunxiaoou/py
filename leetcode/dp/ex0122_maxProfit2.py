#! /usr/local/bin/python3
from typing import List


def maxProfit2(prices: List[int]) -> int:
    n = len(prices)
    i, j, profit = 0, 0, 0
    for j in range(1, n):
        if prices[j] < prices[i]:
            i = j
        elif j + 1 < n and prices[j] > prices[j + 1]:
            profit += prices[j] - prices[i]
            i = j
    # print(i, j)
    if prices[j] > prices[i]:
        profit += prices[j] - prices[i]
    return profit


# 2 dimensions dp:
# dp[0][i] - current max profit without stock (sold already)
# dp[0][i] - current max profit with stock (bought already)
def maxProfit(prices: List[int]) -> int:
    n = len(prices)
    if n < 2:
        return 0
    dp = [[0] * n for _ in range(2)]
    dp[0][0] = 0                # rest on first day
    dp[1][0] = -prices[0]       # buy on first day
    for i in range(1, n):
        dp[0][i] = max(dp[0][i - 1], dp[1][i - 1] + prices[i])
        dp[1][i] = max(dp[1][i - 1], dp[0][i - 1] - prices[i])
    # print(dp[0])
    # print(dp[1])
    return dp[0][-1]


def main():
    print(maxProfit([7, 1, 5, 3, 6, 4]))    # 7
    # [7,   1,  5, 3, 6, 4]
    # [0,   0,  4, 4, 7, 7]
    # [-7, -1, -1, 1, 1, 3]
    # the best way is: buy on 2nd day, sell on 3rd, buy on 4rd, sell on 5rd
    print(maxProfit([1]))     # 0
    print(maxProfit([1, 2, 3, 4, 5]))       # 4
    print(maxProfit([7, 6, 4, 3, 1]))       # 0


if __name__ == "__main__":
    main()
