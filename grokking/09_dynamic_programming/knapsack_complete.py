#! /usr/local/bin/python3
# In Complete Knapsack Problem, for each item, you can put as many times as you want
from typing import List


def print_dp(nums1: List[int], nums2: List[int], dp: List[List[int]]):
    row0 = ['\\\\'] + [str(i) for i in nums2]
    print(', '.join(row0))
    for i in range(len(nums1)):
        print("{},  {}".format(str(nums1[i]), ', '.join([str(j) for j in dp[i]])))


# 2 dimension dp
def knapsack2(cost: List[int], value: List[int], capacity: int) -> int:
    n = len(value)
    dp = [[0] * (capacity + 1) for _ in range(n)]
    i, j = 0, 0
    for i in range(n):
        for j in range(cost[i], capacity + 1):      # current cell cost >= current item cost
            dp[i][j] = max(dp[i - 1][j], value[i] + dp[i][j - cost[i]])
    print_dp(cost, [j for j in range(capacity + 1)], dp)

    return dp[i][j]


# 1 dimension dp
def knapsack(cost: List[int], value: List[int], capacity: int) -> int:
    n = len(value)

    dp = [0] * (capacity + 1)
    for i in range(n):
        for j in range(cost[i], capacity + 1):
            dp[j] = max(dp[j], dp[j - cost[i]] + value[i])
        print(dp)
    return dp[capacity]


def main():
    print(knapsack2([1, 2, 3, 4], [2, 4, 4, 5], 5))             # 10
    """
    \\, 0, 1, 2, 3, 4, 5
    1,  0, 2, 2, 2, 2, 2
    2,  0, 0, 4, 6, 6, 6
    3,  0, 0, 0, 6, 6, 8
    4,  0, 0, 0, 0, 6, 8
    """
    print(knapsack([1, 2, 3, 4], [2, 4, 4, 5], 5))              # 10
    # [0, 2, 4, 6, 8, 10]
    print(knapsack2([4, 3, 1, 1], [30, 20, 15, 20], 4))         # 80
    """
    \\, 0, 1, 2, 3, 4
    4,  0, 0, 0, 0, 30
    3,  0, 0, 0, 20, 30
    1,  0, 15, 30, 45, 60
    1,  0, 20, 40, 60, 80
    """
    print(knapsack([4, 3, 1, 1], [30, 20, 15, 20], 4))          # 80
    # [0, 20, 40, 60, 80]


if __name__ == "__main__":
    main()
