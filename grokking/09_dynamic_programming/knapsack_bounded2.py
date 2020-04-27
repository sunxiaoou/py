#! /usr/local/bin/python3
# In bound Knapsack Problem, for each item, you can put as many times as given quantity
# this is a binary optimized algorithm, which is O(n ^ 2 * log(2, n))
from typing import List


def print_dp(nums1: List[int], nums2: List[int], dp: List[List[int]]):
    row0 = ['\\\\'] + [str(i) for i in nums2]
    print(', '.join(row0))
    for i in range(len(nums1)):
        print("{},  {}".format(str(nums1[i]), ', '.join([str(j) for j in dp[i]])))


def knapsack2(cost: List[int], value: List[int], quantity: List[int], capacity: int) -> int:
    items = []
    for i in range(len(quantity)):
        k = 1
        while quantity[i] >= k:
            items.append((i, k, cost[i] * k, value[i] * k))
            quantity[i] -= k
            k *= 2
        if quantity[i]:
            items.append((i, quantity[i], cost[i] * quantity[i], value[i] * quantity[i]))
    print(items)
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n)]

    for i in range(n):
        _, _, cos, val = items[i]
        for j in range(capacity + 1):
            if j < cos:                     # we need this judgement because cost may bigger than capacity
                dp[i][j] = dp[i - 1][j]
            else:
                dp[i][j] = max(dp[i - 1][j], val + dp[i - 1][j - cos])
    print_dp([cos for _, _, cos, _ in items], [j for j in range(capacity + 1)], dp)

    res = [0] * len(cost)
    j = capacity
    for i in range(n - 1, -1, -1):
        ind, que, cos, _ = items[i]
        if j > 0:
            if i > 0 and dp[i][j] == dp[i - 1][j]:
                continue
            res[ind] += que
            j -= cos
    print(res)

    return dp[-1][-1]


def main():
    print(knapsack2([1, 2, 3, 4], [2, 4, 4, 5], [3, 1, 3, 2], 5))           # 10
    """
    \\, 0, 1, 2, 3, 4, 5
    1,  0, 2, 2, 2, 2, 2
    2,  0, 0, 4, 6, 6, 6
    3,  0, 0, 0, 6, 6, 8
    4,  0, 0, 0, 0, 6, 8
    [3, 1, 0, 0]
    """
    print(knapsack2([4, 3, 1, 1], [30, 20, 15, 20], [1, 2, 2, 3], 4))       # 75
    """
    \\, 0, 1, 2, 3, 4
    4,  0, 0, 0, 0, 30
    3,  0, 0, 0, 20, 30
    1,  0, 15, 30, 30, 35
    1,  0, 20, 40, 60, 75
    [0, 0, 1, 3]
    """


if __name__ == "__main__":
    main()
