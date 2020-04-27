#! /usr/local/bin/python3
# 0/1 knapsack, For each item, you can choose to put or not to put into the knapsack.
#  Therefore, for the number of items, there are only two options: 0 or 1.
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
            dp[i][j] = max(dp[i - 1][j], value[i] + dp[i - 1][j - cost[i]])
    print_dp(cost, [j for j in range(capacity + 1)], dp)

    res = [0] * n
    j = capacity
    for i in range(n - 1, -1, -1):
        if j > 0:
            if i > 0 and dp[i][j] == dp[i - 1][j]:
                continue
            res[i] += 1
            j -= cost[i]
    print(res)

    return dp[-1][-1]


# 1 dimension dp
def knapsack(cost: List[int], value: List[int], capacity: int) -> int:
    n = len(value)

    dp = [0] * (capacity + 1)
    for i in range(n):
        # reverse order since dp[j] needs previous value of dp[j - cost[i])
        for j in range(capacity, cost[i] - 1, -1):
            dp[j] = max(dp[j], dp[j - cost[i]] + value[i])
    print(dp)
    return dp[capacity]


def main():
    print(knapsack2([1, 2, 3, 4], [2, 4, 4, 5], 5))             # 8
    """
    \\, 0, 1, 2, 3, 4, 5
    1,  0, 2, 2, 2, 2, 2
    2,  0, 0, 4, 6, 6, 6
    3,  0, 0, 0, 6, 6, 8
    4,  0, 0, 0, 0, 6, 8
    [0, 1, 1, 0]
    """
    # print(knapsack([1, 2, 3, 4], [2, 4, 4, 5], 5))              # 8
    # [0, 2, 4, 6, 6, 8]
    print(knapsack2([4, 3, 1, 1], [30, 20, 15, 20], 4))         # 40
    """
    \\, 0, 1, 2, 3, 4
    4,  0, 0, 0, 0, 30
    3,  0, 0, 0, 20, 30
    1,  0, 15, 15, 20, 35
    1,  0, 20, 35, 35, 40
    [0, 1, 0, 1]
    """
    # print(knapsack([4, 3, 1, 1], [30, 20, 15, 20], 4))          # 40


if __name__ == "__main__":
    main()
