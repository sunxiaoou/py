#! /usr/local/bin/python3
from typing import List


def maxProfit_slow(prices: List[int]) -> int:
    ps2 = sorted(prices)
    length = len(ps2)
    maximum = 0
    for n in ps2[: length - 1]:
        i = prices.index(n)
        if i < length - 1:
            for n2 in prices[i + 1:]:
                maximum = max(maximum, n2 - n)
    return maximum


def maxProfit(prices: List[int]) -> int:
    if not prices:
        return 0
    profit = 0
    minimum = prices[0]
    for price in prices:
        if price < minimum:
            minimum = price
        else:
            profit = max(profit, price - minimum)
    return profit


def main():
    print(maxProfit([7, 1, 5, 3, 6, 4]))
    print(maxProfit([7, 6, 4, 3, 1]))
    print(maxProfit([9]))


if __name__ == "__main__":
    main()
