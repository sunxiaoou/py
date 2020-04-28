#! /usr/local/bin/python3
# https://www.cnblogs.com/jbelial/articles/2116074.html
# https://www.bilibili.com/video/BV1qt411Z7nE?t=1583&p=2
# https://www.acwing.com/problem/content/7/
# To mix 01, bounded, unbounded (complete) knapsack problems, among them, bounded can convert to 0-1.
from typing import List


def print_dp(nums1: List[int], nums2: List[int], dp: List[List[int]]):
    row0 = ['\\\\'] + [str(i) for i in nums2]
    print(', '.join(row0))
    for i in range(len(nums1)):
        print("{},  {}".format(str(nums1[i]), ', '.join([str(j) for j in dp[i]])))


def knapsack2(cost: List[int], value: List[int], quantity: List[int], capacity: int) -> int:
    items = []
    for i in range(len(quantity)):
        if quantity[i] == -1:               # as 0-1 knapsack item
            items.append((i, 1, cost[i], value[i]))
        elif quantity[i] == 0:              # as unbounded knapsack item
            items.append((i, 0, cost[i], value[i]))
        elif quantity[i] > 0:               # as bounded knapsack item, binary optimized split up
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
        _, qua, cos, val = items[i]
        for j in range(capacity + 1):
            if j < cos:                     # we need this judgement because cost may bigger than capacity
                dp[i][j] = dp[i - 1][j]
            elif not qua:                   # unbounded knapsack item
                dp[i][j] = max(dp[i - 1][j], val + dp[i][j - cos])
            elif qua > 0:                   # 0-1 knapsack item
                dp[i][j] = max(dp[i - 1][j], val + dp[i - 1][j - cos])
    print_dp([cos for _, _, cos, _ in items], [j for j in range(capacity + 1)], dp)

    res = [0] * len(cost)
    j = capacity
    for i in range(n - 1, -1, -1):
        ind, que, cos, _ = items[i]
        while j and not que:
            if i > 0 and dp[i][j] == dp[i - 1][j]:
                break
            res[ind] += 1
            j -= cos
        if j > 0:
            if i > 0 and dp[i][j] == dp[i - 1][j]:
                continue
            res[ind] += que
            j -= cos
    print(res)

    return dp[-1][-1]


def main():
    print(knapsack2([1, 2, 3, 4], [2, 4, 4, 5], [-1, 1, 0, 2], 5))           # 8
    """
    \\, 0, 1, 2, 3, 4, 5
    1,  0, 2, 2, 2, 2, 2
    2,  0, 2, 4, 6, 6, 6
    3,  0, 2, 4, 6, 6, 8
    4,  0, 2, 4, 6, 6, 8
    4,  0, 2, 4, 6, 6, 8
    [0, 1, 1, 0]
    """
    print(knapsack2([4, 3, 1, 1], [30, 20, 20, 15], [-1, 2, 2, 0], 4))       # 70
    """
    \\, 0, 1, 2, 3, 4
    4,  0, 0, 0, 0, 30
    3,  0, 0, 0, 20, 30
    3,  0, 0, 0, 20, 30
    1,  0, 20, 20, 20, 40
    1,  0, 20, 40, 40, 40
    1,  0, 20, 40, 55, 70
    [0, 0, 2, 2]
    """


if __name__ == "__main__":
    main()
