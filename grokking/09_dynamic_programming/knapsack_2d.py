#! /usr/local/bin/python3
# 0/1 knapsack, For each item, you can choose to put or not to put into the knapsack.
#  Therefore, for the number of items, there are only two options: 0 or 1.
from typing import List


def print_dp(nums1: List[int], nums2: List[int], dp: List[List[int]]):
    row0 = ['\\\\'] + [str(i) for i in nums2]
    print(', '.join(row0))
    for i in range(len(nums1)):
        print("{},  {}".format(str(nums1[i]), ', '.join([str(j) for j in dp[i]])))


def knapsack(volume: List[int], weight: List[int], value: List[int], cv: int, cw: int) -> int:
    n = len(value)
    dp = [[0] * (cw + 1) for _ in range(cv + 1)]

    for i in range(n):
        # reverse order since dp[j] needs previous value of dp[j - volume[i])
        for j in range(cv, volume[i] - 1, -1):
            for k in range(cw, weight[i] - 1, -1):
                dp[j][k] = max(dp[j][k], dp[j - volume[i]][k - weight[i]] + value[i])
    print_dp([i for i in range(cv)], [i for i in range(cw)], dp)

    return dp[-1][-1]


def main():
    print(knapsack([1, 2, 3, 4], [2, 4, 4, 5], [3, 4, 5, 6], 5, 6))         # 8
    # [0, 2, 4, 6, 6, 8]
    # print(knapsack([4, 3, 1, 1], [30, 20, 15, 20], 4))          # 40


if __name__ == "__main__":
    main()
