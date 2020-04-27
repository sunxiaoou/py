#! /usr/local/bin/python3
# In bound Knapsack Problem, for each item, you can put as many times as given quantity
# But this is brute force algorithm, which is O(n ** 3)
from typing import List


def print_dp(nums1: List[int], nums2: List[int], dp: List[List[int]]):
    row0 = ['\\\\'] + [str(i) for i in nums2]
    print(', '.join(row0))
    for i in range(len(nums1)):
        print("{},  {}".format(str(nums1[i]), ', '.join([str(j) for j in dp[i]])))


def knapsack2(cost: List[int], value: List[int], quantity: List[int], capacity: int) -> int:
    n = len(value)
    dp = [[0] * (capacity + 1) for _ in range(n)]
    for i in range(n):
        for j in range(cost[i], capacity + 1):
            dp[i][j] = max(dp[i - 1][j],
                           max(value[i] * k + dp[i - 1][j - cost[i] * k]
                               for k in range(quantity[i] + 1) if cost[i] * k <= j))
    print_dp(cost, [j for j in range(capacity + 1)], dp)

    res = [0] * n
    j = capacity
    for i in range(n - 1, -1, -1):
        val = dp[i][j]
        for k in range(quantity[i]):
            if val == value[i] * k + dp[i - 1][j]:
                break
            res[i] += 1
            j -= cost[i]
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
