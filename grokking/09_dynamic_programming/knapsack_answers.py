#! /usr/local/bin/python3
from typing import List

INF = 1000000
MOD = 1000000007


def knapsack_answers(cost: List[int], value: List[int], capacity: int) -> int:
    count = [0] * (capacity + 1)
    count[0] = 1
    dp = [-INF] * (capacity + 1)
    dp[0] = 0
    n = len(value)
    for i in range(n):
        for j in range(capacity, cost[i] - 1, -1):
            v = max(dp[j], dp[j - cost[i]] + value[i])
            c = 0
            if v == dp[j]:
                c += count[j]
            if v == dp[j - cost[i]] + value[i]:
                c += count[j - cost[i]]
            if c >= MOD:
                c -= MOD
            dp[j], count[j] = v, c

    max_val = max(i for i in dp)
    print(max_val)

    res = 0
    for i in range(capacity + 1):
        if dp[i] == max_val:
            res += count[i]
            if res >= MOD:
                res -= MOD
    return res


def main():
    print(knapsack_answers([1, 2, 3, 4], [2, 4, 4, 6], 5))        # 2
    print(knapsack_answers([4, 3, 1, 1], [30, 20, 15, 20], 4))    # 1


if __name__ == "__main__":
    main()
