#! /usr/local/bin/python3
from typing import List


def maxProfit(prices: List[int]) -> int:
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


def main():
    print(maxProfit([1]))     # 0
    print(maxProfit([7, 1, 5, 3, 6, 4]))     # 7
    print(maxProfit([1, 2, 3, 4, 5]))       # 4
    print(maxProfit([7, 6, 4, 3, 1]))       # 0


if __name__ == "__main__":
    main()
